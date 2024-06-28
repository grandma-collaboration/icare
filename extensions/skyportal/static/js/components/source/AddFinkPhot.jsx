import React from "react";
import PropTypes from "prop-types";
import { useSelector, useDispatch } from "react-redux";
import Button from "@mui/material/Button";

import { showNotification } from "baselayer/components/Notifications";
import postFinkPhot from "../../ducks/fink_phot";

const AddPhotFink = ({ id }) => {
  const dispatch = useDispatch();
  const currentUser = useSelector((state) => state.profile);
  const photometry = useSelector((state) => state.photometry[id]);
  const permission =
    currentUser.permissions?.includes("System admin") ||
    currentUser.permissions?.includes("Manage sources") ||
    currentUser.permissions?.includes("Upload data");

  const current_magsys = (phot) => {
    // try to infer the current magsys from the photometry
    if (phot?.length > 0 && typeof phot[0] === "object") {
      return phot[0]?.magsys || "ab";
    }
    return "ab";
  };

  const handleAddPhotFink = (source_id) => {
    dispatch(postFinkPhot(source_id, current_magsys(photometry)))
      .then((result) => {
        if (result.status === "success") {
          dispatch(showNotification("Fink photometry added"));
        } else {
          dispatch(
            showNotification("Fink photometry could not be added", "error")
          );
        }
      })
      .catch((error) => {
        dispatch(
          showNotification(
            `Fink photometry could not be added: ${error}`,
            "error"
          )
        );
      });
  };

  return (
    permission && (
      <Button
        variant="contained"
        size="small"
        onClick={() => {
          handleAddPhotFink(id);
        }}
        data-testid="add-phot-fink"
      >
        Fink Photometry
      </Button>
    )
  );
};

AddPhotFink.propTypes = {
  id: PropTypes.string.isRequired,
};

export default AddPhotFink;
