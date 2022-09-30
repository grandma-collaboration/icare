import React, { useState, useEffect } from "react";
import PropTypes from "prop-types";
import Dialog from "@mui/material/Dialog";
import DialogContent from "@mui/material/DialogContent";
import Button from "./Button";
import { showNotification } from "baselayer/components/Notifications";
import { useDispatch, useSelector } from "react-redux";

import * as sourcestatus from "../ducks/sourcestatus";
import { fetchRecentSources } from "..//ducks/recentSources";

const confirmed_classes = ['Kilonova', 'GRB', 'GW Counterpart']
const rejected_classes = ['Not Kilonova', 'Not GRB', 'Not GW Counterpart']


const SourceStatus = ({ source }) => {
    const [open, setOpen] = useState(false);
    const dispatch = useDispatch();


    const { taxonomyList } = useSelector((state) => state.taxonomies);
    // find the grandma taxonomy, called "Grandma Campaign Source Status"

    const changeSourceStatus = (status) => {
        console.log(status)
        const grandma_taxonomy = taxonomyList.filter((t) => t.name === "Grandma Campaign Source Status")[0];

        if (grandma_taxonomy) {

            dispatch(sourcestatus.updateStatus({
                obj_id: source.obj_id,
                classification: status,
                taxonomy_id: grandma_taxonomy?.id,
                probability: 1.0
            })).then((response) => {
                if (response.status === "success") {
                    dispatch(fetchRecentSources());
                    setOpen(false)
                }
                else {
                    dispatch(showNotification(`Failed to update source status: ${response.message}`, "error"));
                }
            });
        } else {
            dispatch(showNotification("Failed to update source status: no grandma taxonomy found", "error"));
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
                    <h3>
                        Status of {source?.obj_id}
                    </h3>
                    <div style={ {display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gridGap: '1rem'} }>

                        {confirmed_classes.map((c) => (
                            <Button
                                key={c}
                                variant="outlined"
                                size="small"
                                onClick={() => {
                                    changeSourceStatus(c);
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
                                    changeSourceStatus(c);
                                }}
                            >
                                {c}
                            </Button>
                        ))}
                    </div>
                    <br/>
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
