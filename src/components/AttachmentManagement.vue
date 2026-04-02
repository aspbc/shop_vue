<template>
  <div class="attachment-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>素材/附件管理</span>
          <el-upload
            class="upload-demo"
            action="/api/admin/system/attachment/upload"
            :show-file-list="false"
            :on-success="handleUploadSuccess"
            :on-error="handleUploadError"
            :headers="headers"
          >
            <el-button type="primary">上传图片</el-button>
          </el-upload>
        </div>
      </template>

      <el-row :gutter="20">
        <el-col :span="4" v-for="item in attachmentList" :key="item.attId" class="mb-4">
          <el-card :body-style="{ padding: '0px' }" class="image-card">
            <!-- Replace localhost with dynamic URL in production -->
            <img :src="item.attDir" class="image" />
            <div style="padding: 14px">
              <span class="image-name">{{ item.name }}</span>
              <div class="bottom">
                <el-button type="danger" size="small" text @click="handleDelete(item.attId)">删除</el-button>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
      
      <!-- Pagination -->
      <div class="pagination-block">
        <el-pagination
          v-model:current-page="page"
          v-model:page-size="limit"
          :total="total"
          @current-change="fetchAttachments"
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

const attachmentList = ref([])
const page = ref(1)
const limit = ref(18)
const total = ref(0)

const headers = ref({
  Authorization: localStorage.getItem('admin_token') || ''
})

const fetchAttachments = async () => {
  try {
    const res = await axios.get('/api/admin/system/attachment/list', {
      params: { page: page.value, limit: limit.value }
    })
    if (res.data.code === 200) {
      attachmentList.value = res.data.data.records || []
      total.value = res.data.data.total || 0
    }
  } catch (error) {
    ElMessage.error('获取附件失败')
  }
}

const handleUploadSuccess = (res) => {
  if (res.code === 200) {
    ElMessage.success('上传成功')
    fetchAttachments()
  } else {
    ElMessage.error(res.msg || '上传失败')
  }
}

const handleUploadError = () => {
  ElMessage.error('上传失败')
}

const handleDelete = (id) => {
  ElMessageBox.confirm('确定要删除这张图片吗？', '提示', { type: 'warning' }).then(async () => {
    try {
      const res = await axios.delete(`/api/admin/system/attachment/delete/${id}`)
      if (res.data.code === 200) {
        ElMessage.success('删除成功')
        fetchAttachments()
      }
    } catch (error) {
      ElMessage.error('删除失败')
    }
  }).catch(() => {})
}

onMounted(() => {
  fetchAttachments()
})
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.image-card {
  margin-bottom: 20px;
}
.image {
  width: 100%;
  height: 150px;
  object-fit: cover;
  display: block;
}
.image-name {
  font-size: 12px;
  color: #666;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  display: block;
}
.bottom {
  margin-top: 10px;
  line-height: 12px;
  display: flex;
  justify-content: flex-end;
  align-items: center;
}
.pagination-block {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}
</style>
