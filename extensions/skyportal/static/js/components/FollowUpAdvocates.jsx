import React, { useEffect, useState } from "react";
import { useSelector } from "react-redux";
import { Link } from "react-router-dom";
import PropTypes from "prop-types";

import { Paper } from "@mui/material";
import Typography from "@mui/material/Typography";
import DragHandleIcon from "@mui/icons-material/DragHandle";

import dayjs from "dayjs";
import utc from "dayjs/plugin/utc";
import relativeTime from "dayjs/plugin/relativeTime";

dayjs.extend(relativeTime);
dayjs.extend(utc);

const FollowUpAdvocates = ({ classes }) => {
  const currentUser = useSelector((state) => state.profile);
  const shifts = useSelector((state) => state.shifts.shiftList);
  const [currentShift, setCurrentShift] = useState(null);
  const [nextShift, setNextShift] = useState(null);
  const [countdown, setCountdown] = useState(null);

  const timeUntil = (date) => {
    const days = Math.floor(date / (1000 * 60 * 60 * 24));
    const hours = Math.floor((date % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((date % (1000 * 60 * 60)) / (1000 * 60));
    return [days, hours, minutes];
  };

  const getCurrentShift = () => {
    const today = new Date();

    shifts?.forEach((shift) => {
      if (shift.start_date < today && shift.end_date > today) {
        setCurrentShift(shift);
      }
    });
  };

  const getNextShift = () => {
    const nextShifts = [];
    const today = new Date();

    shifts?.forEach((shift) => {
      if (
        shift.shift_users.filter(
          (shift_user) => shift_user.id === currentUser.id
        ).length > 0 &&
        shift.start_date > today
      ) {
        nextShifts.push(shift);
      }
    });
    setNextShift(nextShifts[0]);
  };

  useEffect(() => {
    if (!currentShift) {
      getCurrentShift();
    }

    if (!nextShift) {
      getNextShift();
    } else {
      setCountdown(
        timeUntil(
          new Date(nextShift.start_date).getTime() - new Date().getTime()
        )
      );
      const interval = setInterval(() => {
        setCountdown(
          timeUntil(
            new Date(nextShift.start_date).getTime() - new Date().getTime()
          )
        );
      }, 60000);
      return () => clearInterval(interval);
    }
    return true;
  }, [nextShift, shifts]);

  const weeklyCoordinator = (shift) => {
    const shift_users = shift.shift_users.filter(
      (shift_user) => shift_user.admin === true
    );
    // can modify this to deal with multiple coordinators
    const weekly_Coordinator = `${shift_users[0].first_name}
      ${shift_users[0].last_name}`;
    return weekly_Coordinator;
  };

  // trying to convert CEST to UTC
  const convertToUTC = (date) => {
    const date_UTC = new Date(date);
    const date_UTC_ms =
      date_UTC.getTime() + date_UTC.getTimezoneOffset() * 60000;
    const date_UTC_new = new Date(date_UTC_ms);
    return date_UTC_new;
  };

  return (
    <Paper elevation={1} className={classes.widgetPaperFillSpace}>
      <div className={classes.widgetPaperDiv}>
        <div>
          <Typography variant="h6" display="inline">
            Follow-up Advocates
          </Typography>
          <DragHandleIcon className={`${classes.widgetIcon} dragHandle`} />
          <div>
            {currentShift ? (
              <>
              <Link
                key="currentShift"
                to={`/shifts/${currentShift.id}`}
              >
                <strong>Current Shift</strong>
              </Link>
              <br />
              <Typography variant="body2" display="inline">
                Current Shift: {currentShift.name}
                <br />
                Start date:{" "}
                {dayjs(convertToUTC(currentShift?.start_date)).format(
                  "MMMM Do YYYY, h:mm a"
                )}{" "}
                UTC
                <br />
                End date:{" "}
                {dayjs(convertToUTC(currentShift?.end_date)).format(
                  "MMMM Do YYYY, h:mm a"
                )}{" "}
                UTC
                <br />
                Current Shifters:{" "}
                {currentShift.shift_users?.map(
                  (shift_user) =>
                    `${shift_user.first_name} ${shift_user.last_name}, `
                )}
                <br />
                Weekly Coordinator: {weeklyCoordinator(currentShift)}
                <br />
                <br />
              </Typography>
              </>
            ) : (
              <Typography variant="body2" display="inline">
                No Current Shift
                <br />
                <br />
              </Typography>
            )}
            {nextShift ? (
              <>
                <Link
                  key="currentShift"
                  to={`/shifts/${nextShift.id}`}
                >
                  <strong>My Next Shift</strong>
                </Link>
                <br />
                {countdown && (
                  <Typography variant="body2" display="inline">
                    In: {countdown[0]}d, {countdown[1]}h, {countdown[2]}m<br />
                    Weekly Coordinator: {weeklyCoordinator(nextShift)}
                    <br />
                  </Typography>
                )}
              </>
            ) : (
              <Typography variant="body2" display="inline">
                You have no upcoming shifts
                <br />
                <br />
              </Typography>
            )}
          </div>
        </div>
      </div>
    </Paper>
  );
};

FollowUpAdvocates.propTypes = {
  classes: PropTypes.shape({
    widgetPaperDiv: PropTypes.string.isRequired,
    widgetIcon: PropTypes.string.isRequired,
    widgetPaperFillSpace: PropTypes.string.isRequired,
  }).isRequired,
};

export default FollowUpAdvocates;
