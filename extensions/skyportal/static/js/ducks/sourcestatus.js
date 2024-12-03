import messageHandler from "baselayer/MessageHandler";

import * as API from "../API";
import store from "../store";

export const REFRESH_SOURCE = "skyportal/REFRESH_SOURCE";

const ADD_CLASSIFICATION = "skyportal/ADD_CLASSIFICATION";

export function updateStatus(formData) {
  return API.POST(`/api/classification`, ADD_CLASSIFICATION, formData);
}

// Websocket message handler
messageHandler.add((actionType, payload, dispatch, getState) => {
  const { source } = getState();

  if (actionType === REFRESH_SOURCE) {
    const loaded_obj_key = source?.internal_key;
    if (loaded_obj_key === payload.obj_key) {
      dispatch(fetchSource(source.id));
    }
  }
});
