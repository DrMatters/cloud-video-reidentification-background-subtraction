import React, { Component } from 'react';
import { Checkbox } from '@blueprintjs/core';
import CommentsList from './CommentsList';
import GroupsSelect from './GroupsSelect';

class Comments extends Component {
  constructor(props) {
    super(props);

    this.state = { showClassified: localStorage.getItem('showClassified') === 'true' };

    this.onChange = this.onChange.bind(this);
  }

  componentDidMount() {
    const {
      requestComments, requestGroups, activeGroups, comments, groups,
    } = this.props;

    if (!groups) {
      requestGroups();
    }

    if (!comments) {
      requestComments(activeGroups);
    }
  }

  onChange(selectedOptions) {
    const groupIDs = selectedOptions.map((option) => option.value);

    const { requestComments } = this.props;

    requestComments(groupIDs);
  }

  render() {
    const {
      groups, activeGroups, comments, requestComments, rateComment,
    } = this.props;

    const { showClassified } = this.state;

    return (
      <>
        {groups && (
          <GroupsSelect
            groups={groups}
            activeGroups={activeGroups}
            requestComments={requestComments}
          />
        )}
        <Checkbox
          checked={showClassified}
          onChange={(event) => {
            const { checked } = event.target;
            this.setState(() => ({ showClassified: checked }));
            localStorage.setItem('showClassified', checked.toString());
          }}
        >
          Show classified
        </Checkbox>
        {comments
          ? (
            <CommentsList
              comments={comments}
              groups={groups}
              rateComment={rateComment}
              showClassified={showClassified}
            />
          )
          : (<div>Loading comments...</div>)}
      </>
    );
  }
}

export default Comments;
