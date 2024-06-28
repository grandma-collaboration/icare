import React, { useState } from "react";
import PropTypes from "prop-types";
import Dialog from "@mui/material/Dialog";
import DialogContent from "@mui/material/DialogContent";
import Button from "./Button";
import { showNotification } from "baselayer/components/Notifications";
import { useDispatch, useSelector } from "react-redux";

import * as sourcestatus from "../../ducks/sourcestatus";
import { fetchRecentSources } from "../../ducks/recentSources";

const confirmed_classes = ['Kilonova', 'GRB', 'GW Counterpart', 'GW Candidate', 'Supernova']
const rejected_classes = ['Not Kilonova', 'Not GRB', 'Not GW Counterpart', 'Not GW Candidate', 'Not Supernova']
const not_defined = ["I-care", "Not I-care"]
const obs_status = ["GO GRANDMA", "STOP GRANDMA", "GO GRANDMA (HIGH PRIORITY)"]

const SourceStatus = ({ source }) => {
    const [open, setOpen] = useState(false);
    const dispatch = useDispatch();
    const [clicked, setClicked] = useState(false);
    const { taxonomyList } = useSelector((state) => state.taxonomies);
    // find the grandma taxonomy, called "Grandma Campaign Source Classification"

    const changeSourceClassificationStatus = (status) => {
        const source_status_taxonomy = taxonomyList.filter((t) => t.name === "Grandma Campaign Source Classification")[0];

        if (source_status_taxonomy) {
            const already_has_status = source.classifications.filter((c) => c.taxonomy_id === source_status_taxonomy.id && c.classification === status).length > 0
            if (already_has_status) {
                dispatch(showNotification("Source already has this classification status", "error"));
            } else if (clicked === false) {
                setClicked(true);
                dispatch(sourcestatus.updateStatus({
                    obj_id: source.obj_id,
                    classification: status,
                    taxonomy_id: source_status_taxonomy?.id,
                    probability: 1.0
                })).then((response) => {
                    if (response.status === "success") {
                        dispatch(fetchRecentSources());
                        setClicked(false);
                        setOpen(false);
                    }
                    else {
                        dispatch(showNotification(`Failed to update source status: ${response.message}`, "error"));
                        setClicked(false);
                    }
                });
            } else {
                dispatch(showNotification("You just requested a change in source classification status. Please wait for the request to  be completed.", "warning"));
            }
        } else {
            dispatch(showNotification("Failed to update source status: no grandma taxonomy found", "error"));
            setClicked(false);
        }
    }

    const changeSourceObsStatus = (status) => {
        const source_obs_taxonomy = taxonomyList?.filter((t) => t.name === "Grandma Campaign Source Observation")[0];

        if (source_obs_taxonomy) {
            const already_has_obs = source.classifications.filter((c) => c.taxonomy_id === source_obs_taxonomy.id && c.classification === status).length > 0
            if (already_has_obs) {
                dispatch(showNotification("Source already has this observation status", "error"));
            } else if (clicked === false) {
                setClicked(true);
                dispatch(sourcestatus.updateStatus({
                    obj_id: source.obj_id,
                    classification: status,
                    taxonomy_id: source_obs_taxonomy?.id,
                    probability: 1.0
                })).then((response) => {
                    if (response.status === "success") {
                        dispatch(fetchRecentSources());
                        setClicked(false);
                        setOpen(false)

                    }
                    else {
                        dispatch(showNotification(`Failed to update source status: ${response.message}`, "error"));
                        setClicked(false);
                    }
                });
            } else {
                dispatch(showNotification("You just requested a change in source obs status. Please wait for the request to  be completed.", "warning"));
            }
        } else {
            dispatch(showNotification("Failed to update source status: no grandma taxonomy found", "error"));
            setClicked(false);
        }
    }



    return (
        <div>
            <Button
                variant="outlined"
                size="small"
                onClick={() => setOpen(true)}
            >
                Update Status
            </Button>
            <Dialog open={open}>
                <DialogContent>
                    <div style={ {display: 'grid', gridTemplateColumns: '1fr 1fr', gridGap: '1rem'} }>
                        <div>
                            <h3>
                                Classification Status of {source?.obj_id}
                            </h3>
                            <div style={ {display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gridGap: '1rem'} }>

                                {confirmed_classes.map((c) => (
                                    <Button
                                        key={c}
                                        variant="outlined"
                                        size="small"
                                        onClick={() => {
                                            changeSourceClassificationStatus(c);
                                        }}
                                    >
                                        {c}
                                    </Button>
                                ))}
                                {rejected_classes.map((c) => (
                                    <Button
                                        key={c}
                                        variant="outlined"
                                        size="small"
                                        onClick={() => {
                                            changeSourceClassificationStatus(c);
                                        }}
                                    >
                                        {c}
                                    </Button>
                                ))}
                                {not_defined.map((c) => (
                                    <Button
                                    variant="outlined"
                                    size="small"
                                    onClick={() => {
                                        changeSourceClassificationStatus(c);
                                    }}
                                    >
                                        {c}
                                    </Button>
                                ))}
                            </div>
                        </div>
                        <div>
                            <h3>
                                Source Observation Status
                            </h3>
                            <div style={ {display: 'grid', gridTemplateColumns: '1fr', gridGap: '1rem'} }>
                            {obs_status.map((c) => (
                                    <Button
                                        key={c}
                                        variant="outlined"
                                        size="small"
                                        onClick={() => {
                                            changeSourceObsStatus(c);
                                        }}
                                    >
                                        {c}
                                    </Button>
                                ))}
                            </div>
                        </div>
                    </div>
                    <Button
                        variant="contained"
                        color="primary"
                        onClick={() => {
                            setOpen(false);
                        }}
                    >
                        Close
                    </Button>
                </DialogContent>
            </Dialog>
        </div>
    );

}

SourceStatus.propTypes = {
    source: PropTypes.shape({
        obj_id: PropTypes.string.isRequired,
        ra: PropTypes.number.isRequired,
        dec: PropTypes.number.isRequired,
    }).isRequired
};

export default SourceStatus;
