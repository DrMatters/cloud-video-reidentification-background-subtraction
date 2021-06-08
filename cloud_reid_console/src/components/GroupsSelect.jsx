import React, { Component } from 'react';
import {
  Button, Checkbox, InputGroup, Popover,
} from '@blueprintjs/core';
import styled from 'styled-components';

const Content = styled.div`
  padding: 0.5rem;
  background: white;
`;

const List = styled.div`
  background: white;
  padding: 0.5rem;
`;

const ListElement = styled.div`
  margin: 0.5rem;
`;

class GroupsSelect extends Component {
  constructor(props) {
    super(props);
    this.state = { filter: '' };
  }

  render() {
    const { groups, activeGroups, requestComments } = this.props;
    const { filter } = this.state;
    const activeGroupsSet = new Set(activeGroups);

    const filteredGroups = groups && (
      filter.length !== 0
        ? Array.from(groups.values()).filter((group) => group.name.toLowerCase().includes(filter))
        : Array.from(groups.values())
    );

    return (
      <Popover>
        <Button>Select groups</Button>
        <Content>
          <InputGroup
            placeholder="Find group..."
            onChange={(event) => {
              const { value } = event.target;
              this.setState(() => ({ filter: value.trim().toLowerCase() }));
            }}
          />
          <List>
            {filteredGroups.map((group) => (
              <ListElement key={group.id}>
                <Checkbox
                  large
                  checked={activeGroupsSet.has(group.id)}
                  label={group.name}
                  onChange={(event) => requestComments(event.target.checked
                    ? [group.id, ...activeGroups]
                    : activeGroups.filter((g) => g !== group.id))}
                />
              </ListElement>
            ))}
          </List>
        </Content>
      </Popover>
    );
  }
}

export default GroupsSelect;
