import * as API from "../API";

const POST_FINK_PHOTOMETRY = "skyportal/POST_FINK_PHOTOMETRY";

export default function postFinkPhot(id, current_magsys) {
  return API.POST(`/api/sources/${id}/fink`, POST_FINK_PHOTOMETRY, {
    magsys: current_magsys || "ab",
  });
}
