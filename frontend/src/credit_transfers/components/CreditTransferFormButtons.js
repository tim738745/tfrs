import React from 'react';
import PropTypes from 'prop-types';

import * as Lang from '../../constants/langEnUs';
import CREDIT_TRANSACTIONS from '../../constants/routes/CreditTransactions';
import { CREDIT_TRANSFER_STATUS } from '../../constants/values';
import history from '../../app/History';
import ModalDeleteCreditTransfer from './ModalDeleteCreditTransfer';

const CreditTransferFormButtons = props => (
  <div className="credit-transfer-actions">
    <div className="btn-container">
      <button
        className="btn btn-default"
        onClick={() => history.goBack()}
        type="button"
      >
        {Lang.BTN_APP_CANCEL}
      </button>
      {props.actions.includes(Lang.BTN_DELETE) &&
      <button
        className="btn btn-danger"
        data-target="#confirmDelete"
        data-toggle="modal"
        type="button"
      >
        {Lang.BTN_DELETE}
      </button>
      }
      {props.actions.includes(Lang.BTN_EDIT_DRAFT) &&
      <button
        className="btn btn-default"
        onClick={() => history.push(CREDIT_TRANSACTIONS.EDIT.replace(':id', props.id))}
        type="button"
      >
        {Lang.BTN_EDIT_DRAFT}
      </button>
      }
      {props.actions.includes(Lang.BTN_SAVE_DRAFT) &&
      <button
        className="btn btn-default"
        onClick={() => props.changeStatus(CREDIT_TRANSFER_STATUS.draft)}
        type="submit"
      >
        {Lang.BTN_SAVE_DRAFT}
      </button>
      }
      {props.actions.includes(Lang.BTN_SIGN_1_2) &&
      <button
        className="btn btn-primary"
        onClick={() => props.changeStatus(CREDIT_TRANSFER_STATUS.proposed)}
        type="submit"
      >
        {Lang.BTN_SIGN_1_2}
      </button>
      }
      {props.actions.includes(Lang.BTN_ACCEPT) &&
      <button
        className="btn btn-primary"
        onClick={() => props.changeStatus(CREDIT_TRANSFER_STATUS.accepted)}
        type="submit"
      >
        {Lang.BTN_ACCEPT}
      </button>
      }
      {props.actions.includes(Lang.BTN_REFUSE) &&
      <button
        className="btn btn-danger"
        onClick={() => props.changeStatus(CREDIT_TRANSFER_STATUS.refused)}
        type="submit"
      >
        {Lang.BTN_REFUSE}
      </button>
      }
      {props.actions.includes(Lang.BTN_RESCIND) &&
      <button
        className="btn btn-danger"
        onClick={() => props.changeStatus(CREDIT_TRANSFER_STATUS.rescinded)}
        type="submit"
      >
        {Lang.BTN_RESCIND}
      </button>
      }
    </div>
    {props.actions.includes(Lang.BTN_DELETE) &&
    <ModalDeleteCreditTransfer
      deleteCreditTransfer={props.deleteCreditTransfer}
      message="Do you want to delete this draft?"
      selectedId={props.id}
    />
    }
  </div>
);

CreditTransferFormButtons.defaultProps = {
  deleteCreditTransfer: () => {}
};

CreditTransferFormButtons.propTypes = {
  id: PropTypes.number.isRequired,
  changeStatus: PropTypes.func.isRequired,
  deleteCreditTransfer: PropTypes.func,
  actions: PropTypes.arrayOf(PropTypes.string).isRequired
};

export default CreditTransferFormButtons;
