<template>
  <div class="hello">
    <LoginComponent />
  </div>
</template>

<script>
import LoginComponent from "@/components/HomePageComponents/LoginComponent.vue";
export default {
  name: "HomePageView",
  props: {
    msg: String,
  },
  components: {
    LoginComponent,
  },
};
</script>
