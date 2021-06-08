import React, { Component } from 'react';
import {
  Button, ButtonGroup, Card, H6,
} from '@blueprintjs/core';
import styled from 'styled-components';

const CardList = styled.div`
  display: flex;
  align-items: center;
  width: 100%;
  height: 100%;
  flex-direction: column;
  overflow: auto;
  min-height: 0;
`;

const CommentCard = styled(Card)`
  margin: 1rem;
  padding: 0;
  
  display: grid;
  grid-template-columns: auto auto;
  grid-template-rows: auto auto;
  grid-template-areas: 
    "header buttons"
    "body buttons"
    "body buttons"
`;

const StyledButtonGroup = styled(ButtonGroup)`
  grid-area: buttons;
`;

const CardHeader = styled(H6)`
  grid-area: header;
  padding: 0;
  margin: 0.7rem;
`;

const CardBody = styled.div`
  grid-area: body;
  padding: 0;
  margin: 0.7rem;
`;

class CommentsList extends Component {
  render() {
    const {
      comments, groups, rateComment, showClassified,
    } = this.props;

    const commentsToShow = showClassified
      ? comments
      : comments && comments.filter((comment) => (comment.known_class === null));

    return (
      <CardList>
        {commentsToShow && groups && commentsToShow.map((comment) => (
          <CommentCard key={comment.id} elevation={2}>
            <CardHeader>
              {`In "${groups.get(comment.group_id).name}" at ${new Date(comment.date * 1000).toLocaleString()}`}
            </CardHeader>
            <CardBody>{comment.text}</CardBody>
            <StyledButtonGroup vertical>
              <Button
                minimal
                active={comment.known_class === 0}
                intent="danger"
                onClick={() => rateComment(comment.group_id, comment.id, 'negative')}
              >
                Toxic
              </Button>
              <Button
                minimal
                active={comment.known_class === 1}
                intent="success"
                onClick={() => rateComment(comment.group_id, comment.id, 'positive')}
              >
                Non-toxic
              </Button>
              <Button
                minimal
                active={comment.known_class === null}
                onClick={() => rateComment(comment.group_id, comment.id, 'unrated')}
              >
                Unclassified
              </Button>
            </StyledButtonGroup>
          </CommentCard>
        ))}
      </CardList>
    );
  }
}

export default CommentsList;
