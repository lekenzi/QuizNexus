<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
    <p>This is a simple Vue.js component.</p>
  </div>
</template>

<script>
export default {
  name: "ButtonComponent",
  props: {
    msg: String,
  },
};
</script>

<style scoped>
.hello {
  text-align: center;
  margin-top: 50px;
}
</style>
