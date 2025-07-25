<template>
  <div>
    <h3>Question Details</h3>
    <p><strong>Question:</strong> {{ question.question }}</p>
    <p><strong>Options:</strong></p>
    <ul>
      <li v-for="(option, index) in question.options" :key="index">
        {{ option }}
      </li>
    </ul>
    <p><strong>Answer:</strong> {{ question.answer }}</p>
    <p><strong>Marks:</strong> {{ question.marks }}</p>
  </div>
</template>

<script>
export default {
  name: "DisplayQuestion",
  props: {
    question: {
      type: Object,
      required: true,
    },
  },
};
</script>
