<template>
  <div class="role-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>角色组管理</span>
          <el-button type="primary" @click="handleAdd">添加角色</el-button>
        </div>
      </template>

      <el-table :data="roleList" v-loading="loading" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="roleName" label="角色名称" />
        <el-table-column prop="type" label="角色类型">
          <template #default="{ row }">
            <el-tag :type="row.type === 0 ? 'success' : 'warning'">
              {{ row.type === 0 ? '平台' : '供应商' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态">
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
    </el-card>

    <!-- Role Form Dialog -->
    <el-dialog :title="dialogTitle" v-model="dialogVisible" width="500px">
      <el-form :model="form" ref="formRef" label-width="100px">
        <el-form-item label="角色名称" prop="roleName" :rules="[{ required: true, message: '请输入角色名称' }]">
          <el-input v-model="form.roleName"></el-input>
        </el-form-item>
        <el-form-item label="角色类型">
          <el-radio-group v-model="form.type">
            <el-radio :label="0">平台</el-radio>
            <el-radio :label="2">供应商</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="状态">
          <el-switch v-model="form.status" :active-value="1" :inactive-value="0"></el-switch>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitForm">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import axios from 'axios'

const roleList = ref([])
const loading = ref(false)
const dialogVisible = ref(false)
const dialogTitle = ref('')
const formRef = ref(null)

const form = ref({
  id: null,
  roleName: '',
  type: 0,
  status: 1,
  rules: ''
})

const fetchRoles = async () => {
  loading.value = true
  try {
    const res = await axios.get('/api/admin/system/role/list')
    if (res.data.code === 200) {
      roleList.value = res.data.data
    }
  } catch (error) {
    ElMessage.error('获取角色列表失败')
  } finally {
    loading.value = false
  }
}

const handleAdd = () => {
  form.value = { id: null, roleName: '', type: 0, status: 1, rules: '' }
  dialogTitle.value = '添加角色'
  dialogVisible.value = true
}

const handleEdit = (row) => {
  form.value = { ...row }
  dialogTitle.value = '编辑角色'
  dialogVisible.value = true
}

const handleStatusChange = async (row) => {
  try {
    await axios.post('/api/admin/system/role/save', row)
    ElMessage.success('状态更新成功')
  } catch (error) {
    row.status = row.status === 1 ? 0 : 1 // revert
    ElMessage.error('状态更新失败')
  }
}

const handleDelete = (id) => {
  ElMessageBox.confirm('确定要删除此角色吗？', '提示', { type: 'warning' }).then(async () => {
    try {
      const res = await axios.delete(`/api/admin/system/role/delete/${id}`)
      if (res.data.code === 200) {
        ElMessage.success('删除成功')
        fetchRoles()
      }
    } catch (error) {
      ElMessage.error('删除失败')
    }
  }).catch(() => {})
}

const submitForm = () => {
  formRef.value.validate(async (valid) => {
    if (valid) {
      try {
        const res = await axios.post('/api/admin/system/role/save', form.value)
        if (res.data.code === 200) {
          ElMessage.success('保存成功')
          dialogVisible.value = false
          fetchRoles()
        }
      } catch (error) {
        ElMessage.error('保存失败')
      }
    }
  })
}

onMounted(() => {
  fetchRoles()
})
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
