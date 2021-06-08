import { combineReducers } from 'redux';
import authReducer from './auth';
import commentsReducer from './comments';

export default combineReducers({
  auth: authReducer,
  comments: commentsReducer,
});
