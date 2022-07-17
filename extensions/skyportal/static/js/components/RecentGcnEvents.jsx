import React, { useEffect, useState } from "react";
import { useSelector, useDispatch } from "react-redux";
import { Link } from "react-router-dom";
import PropTypes from "prop-types";

import { makeStyles } from "@material-ui/core/styles";

import Paper from "@mui/material/Paper";
import Typography from "@mui/material/Typography";
import DragHandleIcon from "@mui/icons-material/DragHandle";
import Button from "@mui/material/Button";

import Select from "@material-ui/core/Select";
import MenuItem from "@material-ui/core/MenuItem";
import FormControl from "@material-ui/core/FormControl";

import dayjs from "dayjs";
import utc from "dayjs/plugin/utc";
import relativeTime from "dayjs/plugin/relativeTime";

import * as profileActions from "../ducks/profile";
import * as recentGcnEventsActions from "../ducks/recentGcnEvents";
import * as sourcesActions from "../ducks/sources";
import WidgetPrefsDialog from "./WidgetPrefsDialog";
import GcnTags from "./GcnTags";

dayjs.extend(relativeTime);
dayjs.extend(utc);

const useStyles = makeStyles((theme) => ({
  header: {},
  eventListContainer: {
    height: "calc(100% - 5rem)",
    overflowY: "auto",
    marginTop: "0.625rem",
    paddingTop: "0.625rem",
  },
  eventList: {
    display: "block",
    alignItems: "center",
    listStyleType: "none",
    paddingLeft: 0,
    marginTop: 0,
  },
  eventNameContainer: {
    display: "flex",
    flexDirection: "row",
    alignItems: "center",
  },
  eventNameLink: {
    color: theme.palette.primary.main,
  },
  eventTags: {
    marginLeft: "1rem",
    "& > div": {
      margin: "0.25rem",
      color: "white",
      background: theme.palette.primary.main,
    },
  },
  eventSources: {
    display: "flex",
    flexDirection: "row",
    alignItems: "center",
  },
}));

const defaultPrefs = {
  maxNumEvents: "5",
};

const RecentGcnEvents = ({ classes }) => {
  const styles = useStyles();
  const [gcnEventsSources, setGcnEventsSources] = useState([]);
  const [recentGcnSources, setRecentGcnSources] = useState("");

  const gcnEvents = useSelector((state) => state.recentGcnEvents);
  const recentEvents =
    useSelector((state) => state.profile.preferences?.recentGcnEvents) ||
    defaultPrefs;

  const recentEventSources = useSelector(
    (state) => state.sources?.gcnEventSources
  );

  const dispatch = useDispatch();

  useEffect(() => {
    dispatch(recentGcnEventsActions.fetchRecentGcnEvents());
  }, [dispatch]);

  useEffect(() => {
    if (recentEventSources) {
      setRecentGcnSources((state) => ({
        ...state,
        [recentEventSources.sources?.length]: recentEventSources,
      }));
    }
  }, [recentEventSources]);

  const gcnEventSourcesAssociated = (gcnEvent) => {
    dispatch(sourcesActions.fetchGcnEventSources(gcnEvent.dateobs));
  };

  const getGcnEventSources = (gcnEventList) => {
    const gcnEventsSourcesTemp = [];
    gcnEventsSourcesTemp.push(
      gcnEventList.forEach((gcnEvent) => gcnEventSourcesAssociated(gcnEvent))
    );
    setGcnEventsSources(gcnEventsSourcesTemp);
  };

  if (gcnEventsSources?.length === 0 && gcnEvents) {
    getGcnEventSources(gcnEvents);
  } else if (gcnEventsSources?.length > 0 && gcnEvents) {
    setGcnEventsSources(recentEventSources);
  }

  const ITEM_HEIGHT = 48;
  const MenuProps = {
    PaperProps: {
      style: {
        maxHeight: ITEM_HEIGHT * 4.5,
        width: 250,
      },
    },
  };

  const sourcesAssociated = (gcnEvent, index) => {
    let recentGcnSourcesDefined = Object.entries(recentGcnSources)[index] ?? [];
    if (recentGcnSourcesDefined[1]) {
      recentGcnSourcesDefined = recentGcnSourcesDefined[1].sources;
    }
    if (recentGcnSourcesDefined.length > 0) {
      return (
        <div className={styles.eventSources}>
          {recentGcnSources !== "" &&
            Object.values(recentGcnSources).map((gcn, idx) => {
              if (idx === index) {
                return (
                  <FormControl>
                    <Select
                      labelId="sources-within-the-localization-label"
                      id="sources-within-the-localization"
                      MenuProps={MenuProps}
                      defaultValue="More Sources"
                    >
                      <MenuItem disabled value="More Sources">
                        <em>More Sources</em>
                      </MenuItem>
                      {Object.entries(Object.values(gcn)[3]).map((source) => (
                        <Link
                          key={source[1].id}
                          style={{ textDecoration: "none" }}
                          to={`/source/${source[1].id}`}
                        >
                          <MenuItem key={source.id} value={source}>
                            {source[1].id}
                          </MenuItem>
                        </Link>
                      ))}
                    </Select>
                  </FormControl>
                );
              }
              return null;
            })}
        </div>
      );
    }
    return null;
  };

  return (
    <Paper elevation={1} className={classes.widgetPaperFillSpace}>
      <div className={classes.widgetPaperDiv}>
        <div className={styles.header}>
          <Typography variant="h6" display="inline">
            Recent GCN Events and their sources
          </Typography>
          <DragHandleIcon className={`${classes.widgetIcon} dragHandle`} />
          <div className={classes.widgetIcon}>
            <WidgetPrefsDialog
              // Only expose num events
              initialValues={{
                maxNumEvents: recentEvents.maxNumEvents,
              }}
              stateBranchName="recentGcnEvents"
              title="Recent Events Preferences"
              onSubmit={profileActions.updateUserPreferences}
            />
          </div>
        </div>
        <div className={styles.eventListContainer}>
          <p>Displaying most-viewed events</p>
          <ul className={styles.eventList}>
            {gcnEvents?.map((gcnEvent, index) => (
              <li key={gcnEvent.dateobs}>
                <div className={styles.eventNameContainer}>
                  &nbsp; -&nbsp;
                  <Link to={`/gcn_events/${gcnEvent.dateobs}`}>
                    <Button color="primary">
                      {dayjs(gcnEvent.dateobs).format("YYMMDD HH:mm:ss")}
                    </Button>
                  </Link>
                  <div>({dayjs().to(dayjs.utc(`${gcnEvent.dateobs}Z`))})</div>
                  <div className={styles.eventTags}>
                    <GcnTags gcnEvent={gcnEvent} />
                  </div>
                  {recentGcnSources !== "" &&
                    sourcesAssociated(gcnEvent, index)}
                </div>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </Paper>
  );
};

RecentGcnEvents.propTypes = {
  classes: PropTypes.shape({
    widgetPaperDiv: PropTypes.string.isRequired,
    widgetIcon: PropTypes.string.isRequired,
    widgetPaperFillSpace: PropTypes.string.isRequired,
  }).isRequired,
};

export default RecentGcnEvents;
