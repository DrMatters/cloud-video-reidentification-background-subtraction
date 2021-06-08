import React, { Component } from 'react';
import styled from 'styled-components';
import {
  Button, Card, FormGroup, H3, InputGroup,
} from '@blueprintjs/core';

const Container = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
`;

class Authorized extends Component {
  constructor(props) {
    super(props);
    this.handleForm = this.handleForm.bind(this);
  }

  handleForm(event) {
    event.preventDefault();

    const { login } = this.props;

    const data = new FormData(event.target);
    login(data.get('username'), data.get('password'));
  }

  render() {
    const { isAuthorized, children } = this.props;

    return isAuthorized
      ? children
      : (
        <Container>
          <Card elevation={2}>
            <H3>Login</H3>
            <form onSubmit={this.handleForm} noValidate>
              <FormGroup label="Username" labelFor="username">
                <InputGroup name="username" id="username" autoComplete="username" />
              </FormGroup>
              <FormGroup label="Password" labelFor="password">
                <InputGroup name="password" id="password" type="password" autoComplete="current-password" />
              </FormGroup>
              <Button fill text="Login" type="submit" />
            </form>
          </Card>
        </Container>
      );
  }
}

export default Authorized;
