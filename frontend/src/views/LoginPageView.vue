<template>
  <IndexPageNav />
  <LoginComponent />
</template>

<script>
import IndexPageNav from "@/components/LandingPage/IndexPageNav.vue";
import LoginComponent from "@/components/LandingPage/LoginComponent.vue";
export default {
  name: "HomePageView",
  props: {
    msg: String,
  },
  components: {
    LoginComponent,
    IndexPageNav,
  },
};
</script>
