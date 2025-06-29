<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
    <p>This is a simple Vue.js component.</p>
    <ButtonComponent msg="Click Me!" />
  </div>
</template>

<script>
import ButtonComponent from "@/components/HomePageComponents/ButtonComponent.vue";

export default {
  name: "HomePageView",
  props: {
    msg: String,
  },
  components: {
    ButtonComponent,
  },
};
</script>
