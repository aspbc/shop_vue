<template>
  <div class="product-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>商品管理</span>
          <el-input
            v-model="keyword"
            placeholder="请输入商品名称或关键字"
            style="width: 250px; margin-left: auto; margin-right: 10px;"
            clearable
            @clear="fetchProducts"
            @keyup.enter="fetchProducts"
          />
          <el-select v-model="isShow" placeholder="上架状态" style="width: 120px; margin-right: 10px;" clearable @change="fetchProducts">
            <el-option label="已上架" :value="1" />
            <el-option label="已下架" :value="0" />
          </el-select>
          <el-button type="primary" @click="fetchProducts">搜索</el-button>
          <el-button type="success" @click="handleAdd">发布商品</el-button>
        </div>
      </template>

      <el-table :data="productList" v-loading="loading" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="image" label="商品图片" width="100">
          <template #default="{ row }">
            <el-avatar shape="square" :size="50" :src="row.image" />
          </template>
        </el-table-column>
        <el-table-column prop="storeName" label="商品名称" min-width="200" show-overflow-tooltip />
        <el-table-column prop="price" label="商品售价" width="100" />
        <el-table-column prop="sales" label="销量" width="100" />
        <el-table-column prop="stock" label="库存" width="100" />
        <el-table-column prop="isShow" label="上架状态" width="100">
          <template #default="{ row }">
            <el-switch v-model="row.isShow" :active-value="1" :inactive-value="0" @change="handleStatusChange(row)" />
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="handleEdit(row)">编辑</el-button>
            <el-button size="small" type="danger" @click="handleDelete(row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- Pagination -->
      <div class="pagination-block">
        <el-pagination
          v-model:current-page="page"
          v-model:page-size="limit"
          :total="total"
          @current-change="fetchProducts"
          layout="total, prev, pager, next"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import axios from 'axios'

const productList = ref([])
const loading = ref(false)
const keyword = ref('')
const isShow = ref(null)
const page = ref(1)
const limit = ref(15)
const total = ref(0)

const fetchProducts = async () => {
  loading.value = true
  try {
    const res = await axios.get('/api/admin/store/product/list', {
      params: { page: page.value, limit: limit.value, keyword: keyword.value, isShow: isShow.value }
    })
    if (res.data.code === 200) {
      productList.value = res.data.data.records
      total.value = res.data.data.total
    }
  } catch (error) {
    ElMessage.error('获取商品列表失败')
  } finally {
    loading.value = false
  }
}

const handleAdd = () => {
  ElMessage.info('暂未实现商品发布表单')
}

const handleEdit = (row) => {
  ElMessage.info('暂未实现商品编辑表单')
}

const handleStatusChange = async (row) => {
  try {
    await axios.post('/api/admin/store/product/save', row)
    ElMessage.success('商品状态更新成功')
  } catch (error) {
    row.isShow = row.isShow === 1 ? 0 : 1
    ElMessage.error('商品状态更新失败')
  }
}

const handleDelete = (id) => {
  ElMessageBox.confirm('确定要删除此商品吗？', '提示', { type: 'warning' }).then(async () => {
    try {
      const res = await axios.delete(`/api/admin/store/product/delete/${id}`)
      if (res.data.code === 200) {
        ElMessage.success('删除成功')
        fetchProducts()
      }
    } catch (error) {
      ElMessage.error('删除失败')
    }
  }).catch(() => {})
}

onMounted(() => {
  fetchProducts()
})
</script>

<style scoped>
.card-header {
  display: flex;
  align-items: center;
}
.pagination-block {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}
</style>
