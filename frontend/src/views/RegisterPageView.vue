<template>
  <IndexPageNav />
  <RegisterComponent />
</template>

<script>
import IndexPageNav from "@/components/LandingPage/IndexPageNav.vue";
import RegisterComponent from "@/components/LandingPage/RegisterComponent.vue";
export default {
  name: "RegisterPageView",
  components: {
    IndexPageNav,
    RegisterComponent,
  },
};
</script>
<style scoped></style>
