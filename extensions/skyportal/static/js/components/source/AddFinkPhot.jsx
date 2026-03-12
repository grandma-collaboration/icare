import React, { useState } from "react";
import PropTypes from "prop-types";
import { useSelector, useDispatch } from "react-redux";
import Button from "@mui/material/Button";
import CircularProgress from "@mui/material/CircularProgress";

import { showNotification } from "baselayer/components/Notifications";
import postFinkPhot from "../../ducks/fink_phot";

const AddPhotFink = ({ id }) => {
  const dispatch = useDispatch();
  const [loading, setLoading] = useState(false);
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
    setLoading(true);
    dispatch(postFinkPhot(source_id, current_magsys(photometry)))
      .then((result) => {
        if (result.status === "success") {
          const n = result.data?.total_points ?? 0;
          if (n === 0) {
            dispatch(
              showNotification(
                `No photometry found in Fink for ${source_id}`,
                "warning"
              )
            );
          } else {
            dispatch(
              showNotification(
                `Added ${n} point${n !== 1 ? "s" : ""} to ${source_id}`
              )
            );
          }
        } else {
          const message = result.message || "unknown error";
          dispatch(
            showNotification(
              `Could not retrieve Fink photometry: ${message}`,
              "error"
            )
          );
        }
      })
      .catch((error) => {
        dispatch(
          showNotification(
            `Could not retrieve Fink photometry: ${error?.message || error}`,
            "error"
          )
        );
      })
      .finally(() => {
        setLoading(false);
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
        disabled={loading}
        startIcon={loading ? <CircularProgress size={14} color="inherit" /> : null}
        data-testid="add-phot-fink"
      >
        {loading ? "Fetching..." : "Fink Photometry"}
      </Button>
    )
  );
};

AddPhotFink.propTypes = {
  id: PropTypes.string.isRequired,
};

export default AddPhotFink;
