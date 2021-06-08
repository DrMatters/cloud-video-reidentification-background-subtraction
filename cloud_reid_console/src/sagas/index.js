import {
  all, call, put, takeLatest, select,
} from 'redux-saga/effects';
import {
  loggedin, receiveComments, receiveGroups, logout, types, setActiveGroups, receiveCommentRate,
} from '../actions';
import {
  authorize, getComments, getGroups, rateComment as rateCommentAPI,
} from '../api';

// function* makeAuthorizedAPIRequest(apiMethod, ...args) {
//   const token = yield select(state => state.auth.token);
//   try {
//     const result = yield call(apiMethod, token, ...args);
//   } catch (e) {
//     console.error(e);
//   }
// }

function* login(action) {
  const token = yield call(authorize, action.username, action.password);

  yield put(loggedin(token));
}

function* requestComments(action) {
  const token = yield select((state) => state.auth.token);

  try {
    const comments = (yield all(action.groupIDs.map(
      (groupID) => call(getComments, token, groupID),
    ))).flat(1);

    yield all([
      put(setActiveGroups(action.groupIDs)),
      put(receiveComments(comments)),
    ]);
  } catch (e) {
    console.error(e);
    yield put(logout());
  }
}

function* requestGroups(action) {
  const token = yield select((state) => state.auth.token);

  try {
    const groups = yield call(getGroups, token);

    yield put(receiveGroups(groups));
  } catch (e) {
    console.error(e);
    yield put(logout());
  }
}

function* rateComment(action) {
  const token = yield select((state) => state.auth.token);

  const { groupID, commentID, rate } = action;

  try {
    const comment = yield call(rateCommentAPI, token, groupID, commentID, rate);
    yield put(receiveCommentRate(commentID, comment));
  } catch (e) {
    console.error(e);
    yield put(logout());
  }
}

function* rootSaga() {
  yield all([
    takeLatest(types.LOGIN, login),
    takeLatest(types.REQUEST_COMMENTS, requestComments),
    takeLatest(types.REQUEST_GROUPS, requestGroups),
    takeLatest(types.RATE_COMMENT, rateComment),
  ]);
}

export default rootSaga;
