import React, { lazy, Suspense } from "react";
import { useSelector, useDispatch } from "react-redux";
import makeStyles from "@mui/styles/makeStyles";
import Paper from "@mui/material/Paper";
import CircularProgress from "@mui/material/CircularProgress";
import { Tooltip } from "@mui/material";
import HelpOutlineOutlinedIcon from "@mui/icons-material/HelpOutlineOutlined";
// lazy import the TelescopeMap component
const TelescopeMap = lazy(() => import("./TelescopeMap"));

const useStyles = makeStyles((theme) => ({
  help: {
    display: "flex",
    justifyContent: "right",
    alignItems: "center",
  },
  tooltip: {
    maxWidth: "60rem",
    fontSize: "1.2rem",
  },
  tooltipContent: {
    display: "flex",
    flexDirection: "column",
    justifyContent: "center",
    alignItems: "center",
    width: "100%",
  },
  legend: {
    width: "100%",
    display: "flex",
    flexDirection: "row",
    justifyContent: "left",
    alignItems: "center",
    gap: "10px",
  },
  circle: {
    borderRadius: "50%",
    width: "25px",
    height: "25px",
    display: "inline-block",
  },
  rect: {
    width: "25px",
    height: "25px",
    display: "inline-block",
  },
}));

const TelescopeMapDashboard = () => {
  const dispatch = useDispatch();
  const classes = useStyles();
  const { telescopeList } = useSelector((state) => state.telescopes);

  const Title = () => (
    <div className={classes.tooltipContent}>
      <div className={classes.legend}>
        <div style={{ background: "#f9d71c" }} className={classes.circle} />
        <p> Daytime</p>
      </div>
      <div className={classes.legend}>
        <div style={{ background: "#0c1445" }} className={classes.circle} />
        <p> Nighttime</p>
      </div>
      <div className={classes.legend}>
        <div style={{ background: "#5ca9d6" }} className={classes.rect} />
        <p> Networks and Space-based Instruments</p>
      </div>
    </div>
  );
  
  const TelescopeToolTip = () => (
    <Tooltip
      title={Title()}
      placement="bottom-end"
      classes={{ tooltip: classes.tooltip }}
    >
      <HelpOutlineOutlinedIcon />
    </Tooltip>
  );

  return (
    <Suspense
      fallback={
        <div>
          <CircularProgress color="secondary" />
        </div>
      }
    >
      <Paper>
        <TelescopeMap telescopes={telescopeList} />
        <div className={classes.help}>
          <TelescopeToolTip />
        </div>
      </Paper>
    </Suspense>
  );
};

export default TelescopeMapDashboard;
