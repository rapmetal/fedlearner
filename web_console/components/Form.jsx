import React, { useState } from 'react';
import css from 'styled-jsx/css';
import { Button, Card, Grid, Text, Input, Toggle, Textarea, Note, useTheme } from '@zeit-ui/react';

function useStyles(theme) {
  return css`
    .heading {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-top: ${theme.layout.pageMargin};
    }

    .footer {
      display: flex;
      align-items: center;
      justify-content: space-between;
      width: 100%;
    }
  `;
}

/**
 * interface IField {
 *   key: string;
 *   value?: any;
 *   type?: 'string' | 'boolean' | 'text' | 'password';
 *   label?: string;
 *   required?: boolean;
 *   span?: number; // Grid layout prop
 *   props?: any;
 * }
 */

export default function Form({
  title, onOk, onSubmit, onCancel, gap = 2,
  fields = [], okText = 'Submit', cancelText = 'Cancel',
  message = 'Please fill out the form before submitting.',
}) {
  const theme = useTheme();
  const styles = useStyles(theme);
  const [form, setForm] = useState(fields.reduce((total, current) => {
    total[current.key] = current.value;
    return total;
  }, {}));
  const disabled = fields.filter((x) => x.required).some((x) => !form[x.key]);
  const updateForm = (key, value) => {
    const data = {
      ...form,
      [key]: value,
    };
    setForm(data);
  };
  const renderField = ({ key, label, props, type }) => {
    if (type === 'password') {
      return (
        <Input.Password
          value={form[key]}
          onChange={(e) => updateForm(key, e.target.value)}
          {...props}
        >{label || key}</Input.Password>
      );
    }

    if (type === 'text') {
      return (
        <Textarea
          value={form[key]}
          onChange={(e) => updateForm(key, e.target.value)}
          {...props}
        >{label || key}</Textarea>
      );
    }

    if (type === 'boolean') {
      return (
        <div className="formItemWithLabel">
          <label className="formItemLabel" htmlFor={key}>{label || key}</label>
          <div className="formItemValue">
            <Toggle
              size="large"
              checked={form[key]}
              onChange={(e) => updateForm(key, e.target.checked)}
              {...props}
            />
          </div>
        </div>
      );
    }

    return (
      <Input
        value={form[key]}
        onChange={(e) => updateForm(key, e.target.value)}
        {...props}
      >{label || key}</Input>
    );
  };
  const [error, setError] = useState(null);
  const [submitting, setSubmitting] = useState(false);
  const handleSubmit = async () => {
    setSubmitting(true);
    try {
      const res = await onSubmit(form);
      if (res.error) {
        throw new Error(res.error);
      }
      setSubmitting(false);
      onOk(res.data);
    } catch (err) {
      setSubmitting(false);
      setError(err.message);
    }
  };

  return (
    <>
      <div className="heading">
        <Text h2>{title}</Text>
        <Button auto onClick={onCancel}>{cancelText}</Button>
      </div>
      <Card shadow>
        <Grid.Container gap={gap}>
          {fields.map((x) => <Grid key={x.key} xs={x.span || 8} md={x.span || 8}>{renderField(x)}</Grid>)}
        </Grid.Container>
        <Card.Footer className="formCardFooter">
          {error ? <Note small label="error" type="error">{error}</Note> : <Text p>{message}</Text>}
          <Button auto disabled={disabled} loading={submitting} type="secondary" onClick={handleSubmit}>
            {okText}
          </Button>
        </Card.Footer>
      </Card>

      <style jsx>{styles}</style>
    </>
  );
}
