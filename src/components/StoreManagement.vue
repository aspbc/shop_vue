<template>
  <div class="store-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>门店管理</span>
          <el-button type="primary" @click="handleAdd">添加门店</el-button>
        </div>
      </template>

      <el-table :data="storeList" v-loading="loading" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="image" label="门店图片" width="100">
          <template #default="{ row }">
            <el-avatar shape="square" :size="50" :src="row.image" />
          </template>
        </el-table-column>
        <el-table-column prop="name" label="门店名称" />
        <el-table-column prop="phone" label="联系电话" />
        <el-table-column prop="dayTime" label="营业时间" />
        <el-table-column prop="isShow" label="状态">
          <template #default="{ row }">
            <el-switch v-model="row.isShow" :active-value="1" :inactive-value="0" @change="handleStatusChange(row)" />
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200">
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
          @current-change="fetchStores"
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

const storeList = ref([])
const loading = ref(false)
const page = ref(1)
const limit = ref(15)
const total = ref(0)

const fetchStores = async () => {
  loading.value = true
  try {
    const res = await axios.get('/api/admin/system/store/list', {
      params: { page: page.value, limit: limit.value }
    })
    if (res.data.code === 200) {
      storeList.value = res.data.data.records
      total.value = res.data.data.total
    }
  } catch (error) {
    ElMessage.error('获取门店列表失败')
  } finally {
    loading.value = false
  }
}

const handleAdd = () => {
  ElMessage.info('暂未实现表单弹窗')
}

const handleEdit = (row) => {
  ElMessage.info('暂未实现表单弹窗')
}

const handleStatusChange = async (row) => {
  try {
    await axios.post('/api/admin/system/store/save', row)
    ElMessage.success('状态更新成功')
  } catch (error) {
    row.isShow = row.isShow === 1 ? 0 : 1
    ElMessage.error('状态更新失败')
  }
}

const handleDelete = (id) => {
  ElMessageBox.confirm('确定要删除此门店吗？', '提示', { type: 'warning' }).then(async () => {
    try {
      const res = await axios.delete(`/api/admin/system/store/delete/${id}`)
      if (res.data.code === 200) {
        ElMessage.success('删除成功')
        fetchStores()
      }
    } catch (error) {
      ElMessage.error('删除失败')
    }
  }).catch(() => {})
}

onMounted(() => {
  fetchStores()
})
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.pagination-block {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}
</style>
