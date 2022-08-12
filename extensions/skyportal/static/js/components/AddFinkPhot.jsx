import React from "react";
import PropTypes from "prop-types";
import { useSelector, useDispatch } from "react-redux";
import Button from "@mui/material/Button";
import { showNotification } from "baselayer/components/Notifications";
import postFinkPhot from "../ducks/fink_phot";

const AddPhotFink = ({ id }) => {
  const dispatch = useDispatch();
  const currentUser = useSelector((state) => state.profile);
  const permission =
    currentUser.permissions?.includes("System admin") ||
    currentUser.permissions?.includes("Manage sources") ||
    currentUser.permissions?.includes("Upload data");

  const handleAddPhotFink = (source_id) => {
    dispatch(postFinkPhot(source_id))
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
        onClick={() => {
          handleAddPhotFink(id);
        }}
        data-testid="show-photometry-table-button"
      >
        Add Phot from Fink
      </Button>
    )
  );
};

AddPhotFink.propTypes = {
  id: PropTypes.string.isRequired,
};

export default AddPhotFink;
