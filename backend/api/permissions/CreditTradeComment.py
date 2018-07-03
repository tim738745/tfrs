"""
    REST API Documentation for the NRS TFRS Credit Trading Application

    The Transportation Fuels Reporting System is being designed to streamline
    compliance reporting for transportation fuel suppliers in accordance with
    the Renewable & Low Carbon Fuel Requirements Regulation.

    OpenAPI spec version: v1

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""
from collections import defaultdict
from enum import Enum, auto

from rest_framework import permissions
from api.services.CreditTradeService import CreditTradeService


class CreditTradeCommentPermissions(permissions.BasePermission):
    """Used by Viewset to check permissions for API requests"""

    class _Relationship(Enum):
        Initiator = auto()
        Respondent = auto()
        GovernmentAnalyst = auto()
        GovernmentDirector = auto()

    action_mapping = defaultdict(lambda: False)

    # Key (Relationship, Status, Rescinded?, Privileged?)

    action_mapping[(_Relationship.Initiator, 'Draft', False, False)] = True
    action_mapping[(_Relationship.Initiator, 'Submitted', True, False)] = True
    action_mapping[(_Relationship.Initiator, 'Accepted', True, False)] = True
    action_mapping[(_Relationship.Initiator, 'Recommended', True, False)] = True
    action_mapping[(_Relationship.Initiator, 'Not Recommended', True, False)] = True

    action_mapping[(_Relationship.Respondent, 'Submitted', False, False)] = True
    action_mapping[(_Relationship.Respondent, 'Accepted', True, False)] = True
    action_mapping[(_Relationship.Respondent, 'Recommended', True, False)] = True
    action_mapping[(_Relationship.Respondent, 'Not Recommended', True, False)] = True

    action_mapping[(_Relationship.GovernmentAnalyst, 'Accepted', False, False)] = True
    action_mapping[(_Relationship.GovernmentAnalyst, 'Recommended', False, False)] = True
    action_mapping[(_Relationship.GovernmentAnalyst, 'Not Recommended', False, False)] = True
    action_mapping[(_Relationship.GovernmentAnalyst, 'Accepted', True, False)] = True
    action_mapping[(_Relationship.GovernmentAnalyst, 'Recommended', True, False)] = True
    action_mapping[(_Relationship.GovernmentAnalyst, 'Not Recommended', True, False)] = True
    action_mapping[(_Relationship.GovernmentAnalyst, 'Accepted', False, True)] = True
    action_mapping[(_Relationship.GovernmentAnalyst, 'Recommended', False, True)] = True
    action_mapping[(_Relationship.GovernmentAnalyst, 'Not Recommended', False, True)] = True
    action_mapping[(_Relationship.GovernmentAnalyst, 'Accepted', True, True)] = True
    action_mapping[(_Relationship.GovernmentAnalyst, 'Recommended', True, True)] = True
    action_mapping[(_Relationship.GovernmentAnalyst, 'Not Recommended', True, True)] = True

    action_mapping[(_Relationship.GovernmentDirector, 'Recommended', False, False)] = True
    action_mapping[(_Relationship.GovernmentDirector, 'Not Recommended', False, False)] = True
    action_mapping[(_Relationship.GovernmentDirector, 'Recommended', True, False)] = True
    action_mapping[(_Relationship.GovernmentDirector, 'Not Recommended', True, False)] = True
    action_mapping[(_Relationship.GovernmentDirector, 'Recommended', False, True)] = True
    action_mapping[(_Relationship.GovernmentDirector, 'Not Recommended', False, True)] = True
    action_mapping[(_Relationship.GovernmentDirector, 'Recommended', True, True)] = True
    action_mapping[(_Relationship.GovernmentDirector, 'Not Recommended', True, True)] = True

    @staticmethod
    def user_can_comment(user, credit_trade, privileged):
        """
        This functionality is also used by CreditTradeCommentActions.

        (Which is used by the serializer to to present available options to the user. DRY.)
        """
        is_government = user.organization.id == 1

        relationship = None

        if credit_trade.initiator.id == user.organization.id:
            relationship = CreditTradeCommentPermissions._Relationship.Initiator
        if credit_trade.respondent.id == user.organization.id:
            relationship = CreditTradeCommentPermissions._Relationship.Respondent
        if is_government and user.has_perm('RECOMMEND_CREDIT_TRANSFER'):
            relationship = CreditTradeCommentPermissions._Relationship.GovernmentAnalyst
        if is_government and (user.has_perm('APPROVE_CREDIT_TRANSFER')
                              or user.has_perm('DECLINE_CREDIT_TRANSFER')):
            relationship = CreditTradeCommentPermissions._Relationship.GovernmentDirector

        return CreditTradeCommentPermissions.action_mapping[(
            relationship,
            credit_trade.status.status,
            credit_trade.is_rescinded,
            privileged
        )]

    def has_permission(self, request, view):
        """Check permissions When an object does not yet exist (POST)"""
        # Fallback to has_object_permission unless it's a POST
        if request.method != 'POST':
            return True

        # Need this information to make a decision
        if not (('privileged_access' in request.data) and ('credit_trade' in request.data)):
            return False

        credit_trade = request.data['credit_trade']
        privileged_access = request.data['privileged_access']

        # Check if the user is a party to this credit_trade (or Government)
        # using CreditTradeService logic
        found = CreditTradeService.get_organization_credit_trades(request.user.organization) \
            .filter(id=credit_trade).first()

        if not found:
            return False

        return CreditTradeCommentPermissions.user_can_comment(
            request.user,
            found,
            privileged_access
        )

    def has_object_permission(self, request, view, obj):
        """Check permissions When an object does exist (PUT, GET)"""

        # Users can always see and edit their own comments
        if obj.create_user == request.user:
            return True

        # And see but not edit those from their others in their own organization
        if obj.create_user.organization == request.user.organization and \
                request.method in permissions.SAFE_METHODS:
            return True

        # Government roles can always view comments
        # and can view or edit privileged comments with correct permission
        if request.user.role is not None and request.user.role.is_government_role:

            # read
            if request.method in permissions.SAFE_METHODS:
                if obj.privileged_access:
                    return request.user.has_perm('VIEW_PRIVILEGED_COMMENTS')
                return True

            # write
            if request.method not in permissions.SAFE_METHODS:
                if obj.privileged_access:
                    return request.user.has_perm('EDIT_PRIVILEGED_COMMENTS')
                return True

        # not authorized
        return False
