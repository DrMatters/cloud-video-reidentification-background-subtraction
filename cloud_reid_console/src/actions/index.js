import * as types from './types';

export { types };

export const login = (username, password) => ({
  type: types.LOGIN,
  username,
  password,
});

export const loggedin = (token) => ({
  type: types.LOGGEDIN,
  token,
});

export const logout = () => ({
  type: types.LOGOUT,
});

export const requestGroups = () => ({
  type: types.REQUEST_GROUPS,
});

export const receiveGroups = (groups) => ({
  type: types.RECEIVE_GROUPS,
  groups,
});

export const requestComments = (groupIDs) => ({
  type: types.REQUEST_COMMENTS,
  groupIDs,
});

export const receiveComments = (comments) => ({
  type: types.RECEIVE_COMMENTS,
  comments,
});

export const setActiveGroups = (activeGroups) => ({
  type: types.SET_ACTIVE_GROUPS,
  activeGroups,
});

export const rateComment = (groupID, commentID, rate) => ({
  type: types.RATE_COMMENT,
  groupID,
  commentID,
  rate,
});

export const receiveCommentRate = (commentID, comment) => ({
  type: types.RECEIVE_COMMENT_RATE,
  commentID,
  comment,
});
