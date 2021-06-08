import { types } from '../actions';

const initialState = {
  authorized: false,
  token: sessionStorage.getItem('token'),
};

if (initialState.token) {
  initialState.authorized = true;
}

export default (state = initialState, action) => {
  switch (action.type) {
    case types.LOGGEDIN:
      sessionStorage.setItem('token', action.token);
      return {
        ...state,
        authorized: true,
        token: action.token,
      };

    case types.LOGOUT:
      sessionStorage.removeItem('token');
      return {
        ...state,
        authorized: false,
        token: null,
      };

    default:
      return state;
  }
};
