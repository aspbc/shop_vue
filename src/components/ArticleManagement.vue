<template>
  <div class="article-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>文章资讯管理</span>
          <el-button type="primary" @click="handleAdd">添加文章</el-button>
        </div>
      </template>

      <el-table :data="articleList" v-loading="loading" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="imageInput" label="封面" width="100">
          <template #default="{ row }">
            <el-avatar shape="square" :size="50" :src="row.imageInput" />
          </template>
        </el-table-column>
        <el-table-column prop="title" label="文章标题" />
        <el-table-column prop="author" label="作者" width="120" />
        <el-table-column prop="visit" label="浏览量" width="100" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-switch v-model="row.status" :active-value="1" :inactive-value="0" @change="handleStatusChange(row)" />
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
          @current-change="fetchArticles"
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

const articleList = ref([])
const loading = ref(false)
const page = ref(1)
const limit = ref(15)
const total = ref(0)

const fetchArticles = async () => {
  loading.value = true
  try {
    const res = await axios.get('/api/admin/article/list', {
      params: { page: page.value, limit: limit.value }
    })
    if (res.data.code === 200) {
      articleList.value = res.data.data.records
      total.value = res.data.data.total
    }
  } catch (error) {
    ElMessage.error('获取文章列表失败')
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
    await axios.post('/api/admin/article/save', row)
    ElMessage.success('状态更新成功')
  } catch (error) {
    row.status = row.status === 1 ? 0 : 1
    ElMessage.error('状态更新失败')
  }
}

const handleDelete = (id) => {
  ElMessageBox.confirm('确定要删除此文章吗？', '提示', { type: 'warning' }).then(async () => {
    try {
      const res = await axios.delete(`/api/admin/article/delete/${id}`)
      if (res.data.code === 200) {
        ElMessage.success('删除成功')
        fetchArticles()
      }
    } catch (error) {
      ElMessage.error('删除失败')
    }
  }).catch(() => {})
}

onMounted(() => {
  fetchArticles()
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
