<template>
  <div class="category-params-container">
    <el-tabs v-model="activeName" class="top-tabs" @tab-click="handleClick">
      <el-tab-pane label="商品品牌" name="brand">
        <ProductProductBrand v-if="activeName === 'brand'" />
      </el-tab-pane>
      <el-tab-pane label="商品单位" name="unit">
        <ProductUnitlist v-if="activeName === 'unit'" />
      </el-tab-pane>
      <el-tab-pane label="商品参数" name="specs">
        <ProductSpecs v-if="activeName === 'specs'" />
      </el-tab-pane>
      <el-tab-pane label="保障服务" name="ensure">
        <ProductEnsureCreate v-if="activeName === 'ensure'" />
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import ProductProductBrand from './ProductProductBrand.vue'
import ProductUnitlist from './ProductUnitlist.vue'
import ProductSpecs from './ProductSpecs.vue'
import ProductEnsureCreate from './ProductEnsureCreate.vue'

const activeName = ref('brand')

const handleClick = (tab, event) => {
  // tab switched
}
</script>

<style scoped>
.category-params-container {
  padding: 0;
  background: #fff;
  min-height: calc(100vh - 120px);
}
.top-tabs {
  padding: 15px 20px 0;
}
:deep(.el-tabs__header) {
  margin-bottom: 0;
}
:deep(.el-tabs__nav-wrap::after) {
  height: 1px;
  background-color: #e4e7ed;
}
:deep(.el-tab-pane) {
  padding: 20px;
  background-color: #f5f7f9;
  min-height: calc(100vh - 170px);
}
</style>
