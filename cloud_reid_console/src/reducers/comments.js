import { types } from '../actions';

const initialState = {
  activeGroups: JSON.parse(localStorage.getItem('activeGroups')) || [],
  groups: null,
  comments: null,
};

export default (state = initialState, action) => {
  switch (action.type) {
    case types.RECEIVE_GROUPS:
      return {
        ...state,
        groups: new Map(action.groups.map((group) => [group.id, group])),
      };

    case types.RECEIVE_COMMENTS:
      return {
        ...state,
        comments: action.comments,
      };

    case types.SET_ACTIVE_GROUPS:
      localStorage.setItem('activeGroups', JSON.stringify(action.activeGroups));
      return {
        ...state,
        activeGroups: action.activeGroups,
      };

    case types.RECEIVE_COMMENT_RATE:
      return {
        ...state,
        comments: state.comments.map((comment) => (
          comment.id === action.commentID
            ? action.comment
            : comment
        )),
      };

    default:
      return state;
  }
};
