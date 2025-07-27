<template>
  <div class="p-4 flex flex-wrap gap-4 question-grid-item">
    <div
      v-for="n in number_of_questions"
      :key="n"
      class="btn btn-secondary rounded squares-blocks"
    >
      {{ n }}
    </div>
  </div>
</template>

<script>
export default {
  name: "QuestionGridBlock",
  props: {
    quiz_id: {
      type: Number,
      required: true,
    },
  },
  data() {
    return {
      number_of_questions: Array.from({ length: 10 }, (_, i) => i + 1),
    };
  },
  methods: {
    fetchQuizData() {},
  },
  mounted() {
    this.fetchQuizData();
  },
};
</script>

<style scoped>
.question-grid-item {
  display: flex;
  cursor: pointer;
  transition: background-color 0.3s ease;
  justify-content: flex-start;
}

.squares-blocks {
  text-align: center;
  width: 50px;
  height: 50px;
  align-items: center;
  border-radius: 8px;
  box-shadow: rgba(99, 99, 99, 0.2) 0px 2px 8px 0px;
}
</style>
