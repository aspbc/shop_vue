<template>
  <div class="community-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>种草社区管理</span>
          <el-input
            v-model="title"
            placeholder="请输入帖子标题"
            style="width: 250px; margin-left: auto; margin-right: 10px;"
            clearable
            @clear="fetchPosts"
            @keyup.enter="fetchPosts"
          />
          <el-button type="primary" @click="fetchPosts">搜索</el-button>
        </div>
      </template>

      <el-table :data="postList" v-loading="loading" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="image" label="封面" width="100">
          <template #default="{ row }">
            <el-avatar shape="square" :size="50" :src="row.image" />
          </template>
        </el-table-column>
        <el-table-column prop="title" label="帖子标题" min-width="200" show-overflow-tooltip />
        <el-table-column prop="contentType" label="类型" width="100">
          <template #default="{ row }">
            <el-tag :type="row.contentType === 1 ? 'info' : 'success'">
              {{ row.contentType === 1 ? '图文' : '视频' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="likeNum" label="点赞数" width="100" />
        <el-table-column prop="collectNum" label="收藏数" width="100" />
        <el-table-column prop="commentNum" label="评论数" width="100" />
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="handleEdit(row)">详情</el-button>
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
          @current-change="fetchPosts"
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

const postList = ref([])
const loading = ref(false)
const title = ref('')
const page = ref(1)
const limit = ref(15)
const total = ref(0)

const fetchPosts = async () => {
  loading.value = true
  try {
    const res = await axios.get('/api/admin/community/list', {
      params: { page: page.value, limit: limit.value, title: title.value }
    })
    if (res.data.code === 200) {
      postList.value = res.data.data.records
      total.value = res.data.data.total
    }
  } catch (error) {
    ElMessage.error('获取帖子列表失败')
  } finally {
    loading.value = false
  }
}

const handleEdit = (row) => {
  ElMessage.info('暂未实现帖子详情查看')
}

const handleDelete = (id) => {
  ElMessageBox.confirm('确定要删除此帖子吗（如果存在违规）？', '违规处理', { type: 'warning' }).then(async () => {
    try {
      const res = await axios.delete(`/api/admin/community/delete/${id}`)
      if (res.data.code === 200) {
        ElMessage.success('删除成功')
        fetchPosts()
      }
    } catch (error) {
      ElMessage.error('删除失败')
    }
  }).catch(() => {})
}

onMounted(() => {
  fetchPosts()
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
