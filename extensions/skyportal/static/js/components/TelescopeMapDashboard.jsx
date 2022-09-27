import React, { lazy, Suspense } from "react";
import { useSelector, useDispatch } from "react-redux";
import Paper from "@mui/material/Paper";
import CircularProgress from "@mui/material/CircularProgress";
// lazy import the TelescopeMap component
const TelescopeMap = lazy(() => import("./TelescopeMap"));

const TelescopeMapDashboard = () => {
  const dispatch = useDispatch();
  const { telescopeList } = useSelector((state) => state.telescopes);

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
      </Paper>
    </Suspense>
  );
};

export default TelescopeMapDashboard;
