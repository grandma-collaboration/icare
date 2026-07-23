import * as API from "../API";

const ADD_CLASSIFICATION = "skyportal/ADD_CLASSIFICATION";

export function updateStatus(formData: any) {
  return API.POST(`/api/classification`, ADD_CLASSIFICATION, formData);
}

// REFRESH_SOURCE is now bridged to RTK Query cache invalidation in
// skyportal's ducks/source.ts; the old fetchSource handler is gone.
