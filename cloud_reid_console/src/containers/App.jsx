import React, { Component } from 'react';
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';


import * as actions from '../actions';
import Authorized from '../components/Authorized';
import Comments from '../components/Comments';


class App extends Component {
  constructor(props) {
    super(props);

    const { dispatch } = this.props;
    this.boundActionCreators = bindActionCreators(actions, dispatch);
  }

  render() {
    const {
      authorized,
      comments,
      groups,
      activeGroups,
    } = this.props;
    const {
      requestComments, requestGroups, login, setActiveGroups, rateComment,
    } = this.boundActionCreators;

    return (
      <Authorized isAuthorized={authorized} login={login}>
        <Comments
          groups={groups}
          comments={comments}
          requestComments={requestComments}
          requestGroups={requestGroups}
          activeGroups={activeGroups}
          setActiveGroups={setActiveGroups}
          rateComment={rateComment}
        />
      </Authorized>
    );
  }
}

const mapStateToProps = (state) => ({
  authorized: state.auth.authorized,
  comments: state.comments.comments,
  groups: state.comments.groups,
  activeGroups: state.comments.activeGroups,
});

export default connect(mapStateToProps)(App);
