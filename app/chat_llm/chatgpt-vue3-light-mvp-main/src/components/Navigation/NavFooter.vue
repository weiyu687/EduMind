<script lang="ts" setup>

withDefaults(
  defineProps<{
    showBorder?: boolean
  }>(),
  {
    showBorder: false
  }
)

const link = ref('https://github.com/pdsuwwz')

</script>

<template>
  <footer
    class="footer"
    :class="{
      'b-t b-t-solid b-t-#dcdfe6 dark:b-t-#444': showBorder
    }"
  >
    <div
      class="container"
    >
    </div>
  </footer>
</template>

<style lang="scss" scoped>
.footer {
  margin: 0 auto;
  width: 100%;

  --at-apply: select-none;
  --at-apply: flex justify-center;
  --at-apply: 'bg-#fefbff';

  .container {
    padding: 14px 0;

    .text {
      display: flex;
      justify-content: center;
      align-items: center;
      flex-wrap: wrap;
      margin: 0;
      text-align: center;
      line-height: 1;
      font-size: 1em;
      color: #929292;
    }
  }
}

.github-link {
  transition: border 0.3s ease-in-out;
  margin-left: 6px;

  &:hover {
    border-color: #7d7d7d;
  }
}
</style>
