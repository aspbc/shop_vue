<template>
  <div class="supplier-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>供应商管理</span>
          <el-input
            v-model="keyword"
            placeholder="请输入供应商名称或联系电话"
            style="width: 250px; margin-left: auto; margin-right: 10px;"
            clearable
            @clear="fetchSuppliers"
            @keyup.enter="fetchSuppliers"
          />
          <el-button type="primary" @click="fetchSuppliers">搜索</el-button>
          <el-button type="success" @click="handleAdd">添加供应商</el-button>
        </div>
      </template>

      <el-table :data="supplierList" v-loading="loading" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="supplierName" label="供应商名称" min-width="150" />
        <el-table-column prop="name" label="联系人" width="120" />
        <el-table-column prop="phone" label="联系电话" width="150" />
        <el-table-column prop="email" label="邮箱" width="180" />
        <el-table-column prop="isShow" label="状态" width="100">
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
          @current-change="fetchSuppliers"
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

const supplierList = ref([])
const loading = ref(false)
const keyword = ref('')
const page = ref(1)
const limit = ref(15)
const total = ref(0)

const fetchSuppliers = async () => {
  loading.value = true
  try {
    const res = await axios.get('/api/admin/supplier/list', {
      params: { page: page.value, limit: limit.value, keyword: keyword.value }
    })
    if (res.data.code === 200) {
      supplierList.value = res.data.data.records
      total.value = res.data.data.total
    }
  } catch (error) {
    ElMessage.error('获取供应商列表失败')
  } finally {
    loading.value = false
  }
}

const handleAdd = () => {
  ElMessage.info('暂未实现供应商添加表单')
}

const handleEdit = (row) => {
  ElMessage.info('暂未实现供应商编辑表单')
}

const handleStatusChange = async (row) => {
  try {
    await axios.post('/api/admin/supplier/save', row)
    ElMessage.success('状态更新成功')
  } catch (error) {
    row.isShow = row.isShow === 1 ? 0 : 1
    ElMessage.error('状态更新失败')
  }
}

const handleDelete = (id) => {
  ElMessageBox.confirm('确定要删除此供应商吗？', '提示', { type: 'warning' }).then(async () => {
    try {
      const res = await axios.delete(`/api/admin/supplier/delete/${id}`)
      if (res.data.code === 200) {
        ElMessage.success('删除成功')
        fetchSuppliers()
      }
    } catch (error) {
      ElMessage.error('删除失败')
    }
  }).catch(() => {})
}

onMounted(() => {
  fetchSuppliers()
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
