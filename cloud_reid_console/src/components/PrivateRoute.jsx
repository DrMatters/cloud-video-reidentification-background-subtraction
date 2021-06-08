import React from 'react';
import { Redirect, Route } from 'react-router-dom';

const PrivateRoute = ({
  authorized, path, loginPath, ...props
}) => (
  authorized
    ? <Route {...props} />
    : <Redirect to={loginPath} />
);

export default PrivateRoute;
