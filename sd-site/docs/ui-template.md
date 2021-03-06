---
id: ui-template
title: UI Component Template
---

## Usage

{{ Short description }} Files exist under `src\app\components\{{ component folder }}`

## UI Appearance

![alt text](../static/img/examples/image.PNG "{{ Component Snapshot }}")

## Tag Fields

**Identifier**: `app-{{ identifier }}`

### Input

Specify the input:

| Parameter      | Type         | Desc       | Required |
| -------------- | ------------ | ---------- | -------- |
| `{{ object }}` | `{{ type }}` | {{ desc }} | No       |

Add this to the `.html` file. Replace the sections `{{ }}` with the input to be generated.

```html
<app-identifier [input]="{{ input object }}"></app-identifier>
```

OR

```
code
```

Example:

```
example code
```

Add this to the corresponding _.ts_ file.

```javascript
some_function() {
    // code logic
}
```

### Output

There is no output. The card example above will be generated.

OR

| Return           | Type         | Desc       |
| ---------------- | ------------ | ---------- |
| `{{ variable }}` | `{{ type }}` | {{ desc }} |
