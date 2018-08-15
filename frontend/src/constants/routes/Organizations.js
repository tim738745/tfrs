const API = '/api/organizations';
const BASE_PATH = '/organizations';

const ORGANIZATIONS = {
  API,
  BULLETIN: `https://www2.gov.bc.ca/assets/gov/farming-natural-resources-and-industry/electricity-alternative-energy/transportation/renewable-low-carbon-fuels/rlcf-013.pdf`,
  CREDIT_MARKET_REPORT: `https://www2.gov.bc.ca/assets/gov/farming-natural-resources-and-industry/electricity-alternative-energy/transportation/renewable-low-carbon-fuels/rlcf-017.pdf`,
  DETAILS: `${BASE_PATH}/view/:id`,
  EXPORT: `${API}/xls`,
  LIST: BASE_PATH,
  MINE: `${BASE_PATH}/mine`
};

export default ORGANIZATIONS;