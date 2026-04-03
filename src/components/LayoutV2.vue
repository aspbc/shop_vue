<template>
  <el-container class="layout-v2-container">
    <!-- Top Header Navigation -->
    <el-header class="top-header" height="60px">
      <div class="header-logo">
        <img src="https://demo.crmeb.net/admin/img/logo.png" alt="logo" class="logo-img" />
      </div>
      
      <div class="top-nav">
        <div class="top-nav-wrapper">
          <div class="nav-arrow left" @click="scrollMenu('left')" v-if="showScrollArrows">
            <el-icon><ArrowLeft /></el-icon>
          </div>
          <div class="top-nav-scroll" ref="scrollContainer">
            <el-menu
              mode="horizontal"
              :ellipsis="false"
              :default-active="activeTopMenu"
              class="top-menu"
              background-color="transparent"
              text-color="rgba(255,255,255,0.7)"
              active-text-color="#fff"
              @select="handleTopMenuSelect"
            >
              <el-menu-item v-for="(menu, index) in topMenus" :key="index" :index="menu.name">
                {{ menu.name }}
              </el-menu-item>
            </el-menu>
          </div>
          <div class="nav-arrow right" @click="scrollMenu('right')" v-if="showScrollArrows">
            <el-icon><ArrowRight /></el-icon>
          </div>
        </div>
      </div>
      <div class="header-actions">
        <el-icon class="action-icon" @click="toggleTheme" title="切换回旧版UI"><SwitchButton /></el-icon>
        <el-icon class="action-icon"><Search /></el-icon>
        <el-icon class="action-icon"><FullScreen /></el-icon>
        <el-icon class="action-icon"><RefreshRight /></el-icon>
        <el-icon class="action-icon badge-icon">
          <Bell />
          <span class="badge-dot"></span>
        </el-icon>
        <el-tag size="small" type="primary" effect="plain" class="platform-tag">平台</el-tag>
        <el-dropdown trigger="click">
          <span class="user-dropdown">
            <el-avatar size="small" src="https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png" class="user-avatar" />
            <span class="username">admin</span>
          </span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item>个人中心</el-dropdown-item>
              <el-dropdown-item @click="logout" divided>退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </el-header>

    <el-container class="main-body">
      <!-- Left Sidebar (Second Level Menus) -->
      <el-aside :width="isCollapse ? '64px' : '200px'" class="left-sidebar" style="transition: width 0.3s;">
        <div class="sidebar-header">
          <span class="sidebar-title">{{ activeTopMenu }}</span>
          <el-icon class="collapse-icon" @click="isCollapse = !isCollapse">
            <component :is="isCollapse ? 'Expand' : 'Fold'" />
          </el-icon>
        </div>
        <el-menu
          :default-active="route.path"
          class="side-menu"
          text-color="#333"
          active-text-color="#3e75f5"
          :collapse="isCollapse"
          router
        >
          <!-- Dynamic Sub Menus based on activeTopMenu -->
          <template v-if="activeTopMenu === '商城'">
  <el-sub-menu index="/product">
    <template #title>
      <el-icon><Goods /></el-icon>
      <span>商品</span>
    </template>
    <el-menu-item index="/product_product_list">
      <el-icon><Goods /></el-icon>
      <span>商品列表</span>
    </el-menu-item>
    <el-menu-item index="/product_product_classify">
      <el-icon><Goods /></el-icon>
      <span>商品分类</span>
    </el-menu-item>
    <el-menu-item index="/product_product_attr">
      <el-icon><Goods /></el-icon>
      <span>商品规格</span>
    </el-menu-item>
    <el-menu-item index="/product_label">
      <el-icon><Goods /></el-icon>
      <span>商品标签</span>
    </el-menu-item>
    <el-sub-menu index="/product_product_brand">
      <template #title>
        <el-icon><Management /></el-icon>
        <span>类目参数</span>
      </template>
      <el-menu-item index="/product_product_brand">
        <el-icon><Goods /></el-icon>
        <span>商品品牌</span>
      </el-menu-item>
      <el-menu-item index="/product_unitList">
        <el-icon><Goods /></el-icon>
        <span>商品单位</span>
      </el-menu-item>
      <el-menu-item index="/product_specs">
        <el-icon><Goods /></el-icon>
        <span>商品参数</span>
      </el-menu-item>
      <el-menu-item index="/product_ensure">
          <el-icon><CreditCard /></el-icon>
          <span>保障服务</span>
        </el-menu-item>
    </el-sub-menu>
    <el-menu-item index="/setting_system_create">
      <el-icon><OfficeBuilding /></el-icon>
      <span>系统表单</span>
    </el-menu-item>
    <el-menu-item index="/product_product_reply">
      <el-icon><Goods /></el-icon>
      <span>商品评论</span>
    </el-menu-item>
    <el-menu-item index="/product_product_reply_config">
      <el-icon><Setting /></el-icon>
      <span>评论设置</span>
    </el-menu-item>
  </el-sub-menu>
  <el-sub-menu index="/order">
    <template #title>
      <el-icon><List /></el-icon>
      <span>订单</span>
    </template>
    <el-sub-menu index="/order_list">
      <template #title>
        <el-icon><List /></el-icon>
        <span>订单列表</span>
      </template>
      <el-menu-item index="/adminorder_list">
        <el-icon><List /></el-icon>
        <span>订单列表</span>
      </el-menu-item>
    </el-sub-menu>
    <el-menu-item index="/order_refund">
      <el-icon><List /></el-icon>
      <span>售后订单</span>
    </el-menu-item>
  </el-sub-menu>
  <el-sub-menu index="/setting_distribution_deliver">
    <template #title>
      <el-icon><Histogram /></el-icon>
      <span>发货</span>
    </template>
    <el-menu-item index="/setting_distribution_deliver">
      <el-icon><Setting /></el-icon>
      <span>发货设置</span>
    </el-menu-item>
    <el-menu-item index="/setting_freight_shipping_templates_list">
      <el-icon><SoldOut /></el-icon>
      <span>运费模板</span>
    </el-menu-item>
    <el-menu-item index="/setting_freight_express_index">
      <el-icon><Cpu /></el-icon>
      <span>物流公司</span>
    </el-menu-item>
    <el-menu-item index="/setting_delivery_service_index">
      <el-icon><Setting /></el-icon>
      <span>配送员管理</span>
    </el-menu-item>
    <el-menu-item index="/setting_shop_storeList">
      <el-icon><Camera /></el-icon>
      <span>自提点列表</span>
    </el-menu-item>
    <el-menu-item index="/setting_city_delivery_setting">
      <el-icon><Setting /></el-icon>
      <span>配送设置</span>
    </el-menu-item>
    <el-menu-item index="/setting_city_delivery_record">
      <el-icon><Medal /></el-icon>
      <span>配送记录</span>
    </el-menu-item>
    <el-menu-item index="/setting_freight_city_list">
      <el-icon><Document /></el-icon>
      <span>城市数据</span>
    </el-menu-item>
  </el-sub-menu>
  <el-sub-menu index="/setting_shop">
    <template #title>
      <el-icon><Setting /></el-icon>
      <span>商城设置</span>
    </template>
    <el-menu-item index="/setting_shop_product">
      <el-icon><Goods /></el-icon>
      <span>商品设置</span>
    </el-menu-item>
    <el-menu-item index="/setting_shop_trade">
      <el-icon><Setting /></el-icon>
      <span>交易设置</span>
    </el-menu-item>
    <el-menu-item index="/setting_shop_agreemant">
      <el-icon><Sell /></el-icon>
      <span>政策协议</span>
    </el-menu-item>
    <el-menu-item index="/setting_shop_releaseset">
      <el-icon><Setting /></el-icon>
      <span>释放比例设置</span>
    </el-menu-item>
    <el-menu-item index="/setting_shop_coinoffset">
      <el-icon><Setting /></el-icon>
      <span>屏蔽前端代币设置</span>
    </el-menu-item>
  </el-sub-menu>
          </template>
          <template v-if="activeTopMenu === '用户'">
  <el-menu-item index="/statistic_user">
    <el-icon><User /></el-icon>
    <span>用户概况</span>
  </el-menu-item>
  <el-sub-menu index="/user_manage">
    <template #title>
      <el-icon><User /></el-icon>
      <span>用户</span>
    </template>
    <el-menu-item index="/user_list">
      <el-icon><User /></el-icon>
      <span>用户列表</span>
    </el-menu-item>
    <el-menu-item index="/user_group">
      <el-icon><User /></el-icon>
      <span>用户分组</span>
    </el-menu-item>
    <el-menu-item index="/user_label">
      <el-icon><User /></el-icon>
      <span>用户标签</span>
    </el-menu-item>
    <el-menu-item index="/marketing_channel_code">
      <el-icon><Connection /></el-icon>
      <span>渠道码</span>
    </el-menu-item>
    <el-menu-item index="/user_userSet">
      <el-icon><User /></el-icon>
      <span>用户设置</span>
    </el-menu-item>
  </el-sub-menu>
  <el-sub-menu index="/user">
    <template #title>
      <el-icon><User /></el-icon>
      <span>用户运营</span>
    </template>
    <el-menu-item index="/vipuser_level_list">
      <el-icon><User /></el-icon>
      <span>用户等级</span>
    </el-menu-item>
    <el-menu-item index="/user_levelSet">
      <el-icon><Setting /></el-icon>
      <span>等级设置</span>
    </el-menu-item>
    <el-menu-item index="/user_registerSet">
      <el-icon><Guide /></el-icon>
      <span>新人礼包</span>
    </el-menu-item>
    <el-menu-item index="/user_memberGift">
      <el-icon><Wallet /></el-icon>
      <span>激活有礼</span>
    </el-menu-item>
  </el-sub-menu>
  <el-sub-menu index="/marketing_store_coupon">
    <template #title>
      <el-icon><More /></el-icon>
      <span>优惠券</span>
    </template>
    <el-sub-menu index="/marketing_store_coupon_issue_index">
      <template #title>
        <el-icon><Coin /></el-icon>
        <span>优惠券列表</span>
      </template>
    </el-sub-menu>
    <el-menu-item index="/marketing_store_coupon_user_index">
      <el-icon><Notebook /></el-icon>
      <span>领取记录</span>
    </el-menu-item>
  </el-sub-menu>
  <el-sub-menu index="/marketing_integral_system_config_3_11">
    <template #title>
      <el-icon><Grid /></el-icon>
      <span>资产</span>
    </template>
    <el-menu-item index="/marketing_integral_system_config">
      <el-icon><Setting /></el-icon>
      <span>积分配置</span>
    </el-menu-item>
    <el-menu-item index="/marketing_user_point_index">
      <el-icon><Notebook /></el-icon>
      <span>积分日志</span>
    </el-menu-item>
    <el-menu-item index="/marketing_balance_recharge">
      <el-icon><Shop /></el-icon>
      <span>代币金额</span>
    </el-menu-item>
    <el-menu-item index="/integral_release_index">
      <el-icon><Setting /></el-icon>
      <span>积分释放配置</span>
    </el-menu-item>
    <el-menu-item index="/marketing_weather_tpapply">
      <el-icon><More /></el-icon>
      <span>代币审核列表</span>
    </el-menu-item>
    <el-menu-item index="/marketing_weather_tongpiao">
      <el-icon><User /></el-icon>
      <span>用户账单</span>
    </el-menu-item>
  </el-sub-menu>
  <el-sub-menu index="/work">
    <template #title>
      <el-icon><Position /></el-icon>
      <span>企业微信</span>
    </template>
    <el-sub-menu index="/work_client_list">
      <template #title>
        <el-icon><Trophy /></el-icon>
        <span>客户管理</span>
      </template>
      <el-menu-item index="/work_channel_code">
        <el-icon><Connection /></el-icon>
        <span>企微渠道码</span>
      </el-menu-item>
      <el-menu-item index="/work_welcome">
        <el-icon><DataAnalysis /></el-icon>
        <span>欢迎语</span>
      </el-menu-item>
      <el-menu-item index="/work_addWelcome">
        <el-icon><Phone /></el-icon>
        <span>新建好友欢迎语</span>
      </el-menu-item>
      <el-menu-item index="/work_client_list">
        <el-icon><Management /></el-icon>
        <span>客户列表</span>
      </el-menu-item>
      <el-menu-item index="/work_client_group">
        <el-icon><User /></el-icon>
        <span>客户群发</span>
      </el-menu-item>
      <el-menu-item index="/work_client_moment">
        <el-icon><ShoppingCartFull /></el-icon>
        <span>朋友圈列表</span>
      </el-menu-item>
      <el-menu-item index="/work_client_group_info">
        <el-icon><List /></el-icon>
        <span>客户群发详情</span>
      </el-menu-item>
      <el-menu-item index="/work_client_moment_info">
        <el-icon><Medal /></el-icon>
        <span>朋友圈详情</span>
      </el-menu-item>
    </el-sub-menu>
    <el-sub-menu index="/work_client_group_chat">
      <template #title>
        <el-icon><Coin /></el-icon>
        <span>客户群运营</span>
      </template>
      <el-menu-item index="/work_client_group_chat">
        <el-icon><Bell /></el-icon>
        <span>客户群列表</span>
      </el-menu-item>
      <el-menu-item index="/work_auth_group">
        <el-icon><DataLine /></el-icon>
        <span>自动拉群</span>
      </el-menu-item>
      <el-menu-item index="/work_addAuthGroup">
        <el-icon><Star /></el-icon>
        <span>新建自动拉群</span>
      </el-menu-item>
      <el-menu-item index="/work_client_statistical">
        <el-icon><DataAnalysis /></el-icon>
        <span>客户群统计</span>
      </el-menu-item>
      <el-menu-item index="/work_group_template">
        <el-icon><Goods /></el-icon>
        <span>客户群群发</span>
      </el-menu-item>
      <el-menu-item index="/work_group_template_info">
        <el-icon><Camera /></el-icon>
        <span>客户群群发详情</span>
      </el-menu-item>
    </el-sub-menu>
    <el-menu-item index="/work_staffList">
      <el-icon><Document /></el-icon>
      <span>员工列表</span>
    </el-menu-item>
  </el-sub-menu>
  <el-menu-item index="/user_importRecord">
    <el-icon><User /></el-icon>
    <span>用户导入记录</span>
  </el-menu-item>
          </template>
          <template v-if="activeTopMenu === '营销'">
  <el-menu-item index="/marketing_home">
    <el-icon><Present /></el-icon>
    <span>营销中心</span>
  </el-menu-item>
  <el-sub-menu index="/vipuser_grade">
    <template #title>
      <el-icon><Discount /></el-icon>
      <span>付费会员</span>
    </template>
    <el-menu-item index="/vipuser_grade_type">
      <el-icon><Grid /></el-icon>
      <span>会员类型</span>
    </el-menu-item>
    <el-menu-item index="/vipuser_grade_right">
      <el-icon><Star /></el-icon>
      <span>会员权益</span>
    </el-menu-item>
    <el-menu-item index="/vipuser_grade_agreement">
      <el-icon><Cpu /></el-icon>
      <span>会员协议</span>
    </el-menu-item>
    <el-menu-item index="/vipuser_grade_card">
      <el-icon><VideoCamera /></el-icon>
      <span>卡密会员</span>
    </el-menu-item>
    <el-menu-item index="/vipuser_grade_record">
      <el-icon><Star /></el-icon>
      <span>会员记录</span>
    </el-menu-item>
    <el-menu-item index="/vipuser_grade_list">
      <el-icon><Shop /></el-icon>
      <span>会员卡列表</span>
    </el-menu-item>
    <el-menu-item index="/user_svipSet">
      <el-icon><Setting /></el-icon>
      <span>会员设置</span>
    </el-menu-item>
  </el-sub-menu>
  <el-sub-menu index="/marketing_lottery_index">
    <template #title>
      <el-icon><Management /></el-icon>
      <span>抽奖</span>
    </template>
    <el-menu-item index="/marketing_lottery_list">
      <el-icon><Wallet /></el-icon>
      <span>抽奖列表</span>
    </el-menu-item>
    <el-menu-item index="/marketing_lottery_config">
      <el-icon><Setting /></el-icon>
      <span>抽奖配置</span>
    </el-menu-item>
    <el-menu-item index="/marketing_lottery_recording_list">
      <el-icon><Shop /></el-icon>
      <span>中奖记录</span>
    </el-menu-item>
  </el-sub-menu>
  <el-sub-menu index="/marketing_store_combination">
    <template #title>
      <el-icon><TrendCharts /></el-icon>
      <span>拼团</span>
    </template>
    <el-menu-item index="/marketing_store_combination_index">
      <el-icon><Goods /></el-icon>
      <span>拼团商品</span>
    </el-menu-item>
    <el-menu-item index="/marketing_store_combination_combina_list">
      <el-icon><Monitor /></el-icon>
      <span>拼团列表</span>
    </el-menu-item>
    <el-menu-item index="/marketing_store_combination_statistics">
      <el-icon><DataAnalysis /></el-icon>
      <span>拼团统计</span>
    </el-menu-item>
  </el-sub-menu>
  <el-sub-menu index="/marketing_store_seckill">
    <template #title>
      <el-icon><Files /></el-icon>
      <span>秒杀</span>
    </template>
    <el-menu-item index="/marketing_store_seckill_list">
      <el-icon><List /></el-icon>
      <span>秒杀列表</span>
    </el-menu-item>
    <el-menu-item index="/marketing_store_seckill_index">
      <el-icon><Goods /></el-icon>
      <span>秒杀商品</span>
    </el-menu-item>
    <el-menu-item index="/marketing_store_seckill_statistics">
      <el-icon><DataAnalysis /></el-icon>
      <span>秒杀统计</span>
    </el-menu-item>
    <el-menu-item index="/marketing_store_seckill_data_index">
      <el-icon><Setting /></el-icon>
      <span>秒杀配置</span>
    </el-menu-item>
  </el-sub-menu>
  <el-sub-menu index="/marketing_store_bargain">
    <template #title>
      <el-icon><Box /></el-icon>
      <span>砍价</span>
    </template>
    <el-menu-item index="/marketing_store_bargain_index">
      <el-icon><Goods /></el-icon>
      <span>砍价商品</span>
    </el-menu-item>
    <el-menu-item index="/marketing_store_bargain_bargain_list">
      <el-icon><ShoppingCart /></el-icon>
      <span>砍价列表</span>
    </el-menu-item>
    <el-menu-item index="/marketing_store_bargain_setting">
      <el-icon><Setting /></el-icon>
      <span>砍价设置</span>
    </el-menu-item>
    <el-menu-item index="/marketing_store_bargain_statistics">
      <el-icon><DataAnalysis /></el-icon>
      <span>砍价统计</span>
    </el-menu-item>
  </el-sub-menu>
  <el-sub-menu index="/marketing_giftCard">
    <template #title>
      <el-icon><Menu /></el-icon>
      <span>礼品卡</span>
    </template>
    <el-menu-item index="/marketing_giftCard_manage">
      <el-icon><Share /></el-icon>
      <span>生成卡号</span>
    </el-menu-item>
    <el-menu-item index="/marketing_giftCard_index">
      <el-icon><Setting /></el-icon>
      <span>礼品卡列表</span>
    </el-menu-item>
    <el-menu-item index="/marketing_giftCard_record">
      <el-icon><Bell /></el-icon>
      <span>卡密管理</span>
    </el-menu-item>
  </el-sub-menu>
  <el-sub-menu index="/sysytem_automation">
    <template #title>
      <el-icon><ShoppingCartFull /></el-icon>
      <span>自动化运营</span>
    </template>
    <el-menu-item index="/marketing_automation">
      <el-icon><Files /></el-icon>
      <span>智能推送</span>
    </el-menu-item>
    <el-menu-item index="/marketing_birthday">
      <el-icon><Star /></el-icon>
      <span>生日有礼</span>
    </el-menu-item>
  </el-sub-menu>
  <el-sub-menu index="/marketing_discount">
    <template #title>
      <el-icon><Folder /></el-icon>
      <span>促销</span>
    </template>
    <el-menu-item index="/marketing_discount_list">
      <el-icon><Medal /></el-icon>
      <span>限时折扣</span>
    </el-menu-item>
    <el-menu-item index="/marketing_discount_full_discount">
      <el-icon><Share /></el-icon>
      <span>满减满折</span>
    </el-menu-item>
    <el-menu-item index="/marketing_discount_give">
      <el-icon><Box /></el-icon>
      <span>满送活动</span>
    </el-menu-item>
    <el-menu-item index="/marketing_discount_pieces_discount">
      <el-icon><Wallet /></el-icon>
      <span>第N件N折</span>
    </el-menu-item>
    <el-menu-item index="/marketing_store_discounts_index">
      <el-icon><Monitor /></el-icon>
      <span>组合套餐</span>
    </el-menu-item>
  </el-sub-menu>
  <el-sub-menu index="/marketing_user_point">
    <template #title>
      <el-icon><Postcard /></el-icon>
      <span>积分</span>
    </template>
    <el-menu-item index="/marketing_integral_classify">
      <el-icon><DataLine /></el-icon>
      <span>积分分类</span>
    </el-menu-item>
    <el-menu-item index="/marketing_store_integral_index">
      <el-icon><Goods /></el-icon>
      <span>积分商品</span>
    </el-menu-item>
    <el-menu-item index="/marketing_point_statistic">
      <el-icon><DataAnalysis /></el-icon>
      <span>积分统计</span>
    </el-menu-item>
  </el-sub-menu>
  <el-sub-menu index="/marketing_sign">
    <template #title>
      <el-icon><Present /></el-icon>
      <span>签到</span>
    </template>
    <el-menu-item index="/marketing_sign_config">
      <el-icon><Setting /></el-icon>
      <span>签到配置</span>
    </el-menu-item>
    <el-menu-item index="/marketing_sign_rewards">
      <el-icon><Document /></el-icon>
      <span>签到奖励</span>
    </el-menu-item>
  </el-sub-menu>
  <el-sub-menu index="/marketing_activity_background">
    <template #title>
      <el-icon><Medal /></el-icon>
      <span>活动氛围</span>
    </template>
    <el-sub-menu index="/marketing_activity_frame">
      <template #title>
        <el-icon><Monitor /></el-icon>
        <span>活动边框</span>
      </template>
    </el-sub-menu>
    <el-sub-menu index="/marketing_activity_background">
      <template #title>
        <el-icon><Postcard /></el-icon>
        <span>活动背景</span>
      </template>
    </el-sub-menu>
  </el-sub-menu>
          </template>
          <template v-if="activeTopMenu === '分销'">
  <el-sub-menu index="/agent_agent_manage_index">
    <template #title>
      <el-icon><Share /></el-icon>
      <span>分销员</span>
    </template>
    <el-menu-item index="/agent_agent_manage_index">
      <el-icon><Share /></el-icon>
      <span>分销员管理</span>
    </el-menu-item>
    <el-menu-item index="/setting_membership_level_index">
      <el-icon><Share /></el-icon>
      <span>分销员等级</span>
    </el-menu-item>
    <el-menu-item index="/finance_finance_commission">
      <el-icon><User /></el-icon>
      <span>佣金记录</span>
    </el-menu-item>
    <el-menu-item index="/agent_promoter_apply">
      <el-icon><Share /></el-icon>
      <span>分销员申请</span>
    </el-menu-item>
  </el-sub-menu>
  <el-sub-menu index="/setting_system_config_retail_2_9">
    <template #title>
      <el-icon><Setting /></el-icon>
      <span>分销配置</span>
    </template>
    <el-menu-item index="/setting_system_config_retail_2_9">
      <el-icon><Share /></el-icon>
      <span>分销模式</span>
    </el-menu-item>
    <el-menu-item index="/setting_system_config_rake_back">
      <el-icon><Setting /></el-icon>
      <span>返佣设置</span>
    </el-menu-item>
    <el-menu-item index="/agent_agreement">
      <el-icon><Share /></el-icon>
      <span>分销说明</span>
    </el-menu-item>
  </el-sub-menu>
  <el-sub-menu index="/agent_division">
    <template #title>
      <el-icon><Share /></el-icon>
      <span>团队分销</span>
    </template>
    <el-menu-item index="/agent_division_list">
      <el-icon><Guide /></el-icon>
      <span>团队列表</span>
    </el-menu-item>
    <el-menu-item index="/agent_agent_list">
      <el-icon><Sell /></el-icon>
      <span>代理列表</span>
    </el-menu-item>
    <el-menu-item index="/agent_apply_list">
      <el-icon><Shop /></el-icon>
      <span>代理申请</span>
    </el-menu-item>
    <el-menu-item index="/setting_shop_division">
      <el-icon><Setting /></el-icon>
      <span>团队配置</span>
    </el-menu-item>
    <el-menu-item index="/agent_statistics">
      <el-icon><DataAnalysis /></el-icon>
      <span>团队统计</span>
    </el-menu-item>
    <el-menu-item index="/agent_order">
      <el-icon><List /></el-icon>
      <span>团队订单</span>
    </el-menu-item>
  </el-sub-menu>
          </template>
          <template v-if="activeTopMenu === '店铺'">
  <el-sub-menu index="/setting_pages">
    <template #title>
      <el-icon><Shop /></el-icon>
      <span>店铺装修</span>
    </template>
    <el-menu-item index="/setting_pages_devise">
      <el-icon><Notebook /></el-icon>
      <span>首页装修</span>
    </el-menu-item>
    <el-menu-item index="/setting_theme_style">
      <el-icon><Picture /></el-icon>
      <span>主题风格</span>
    </el-menu-item>
    <el-menu-item index="/setting_pages_product_category">
      <el-icon><Goods /></el-icon>
      <span>商品分类</span>
    </el-menu-item>
    <el-menu-item index="/setting_pages_home">
      <el-icon><Headset /></el-icon>
      <span>个人中心</span>
    </el-menu-item>
    <el-menu-item index="/setting_pages_product_detail">
      <el-icon><Goods /></el-icon>
      <span>商品详情</span>
    </el-menu-item>
    <el-menu-item index="/setting_pages_fab">
      <el-icon><Phone /></el-icon>
      <span>悬浮菜单</span>
    </el-menu-item>
  </el-sub-menu>
  <el-sub-menu index="/system_file">
    <template #title>
      <el-icon><MapLocation /></el-icon>
      <span>通用组件</span>
    </template>
    <el-menu-item index="/setting_system_visualization_data">
      <el-icon><More /></el-icon>
      <span>开屏广告</span>
    </el-menu-item>
    <el-menu-item index="/product_hotWords">
      <el-icon><PriceTag /></el-icon>
      <span>搜索热词</span>
    </el-menu-item>
    <el-menu-item index="/system_file">
      <el-icon><MapLocation /></el-icon>
      <span>素材中心</span>
    </el-menu-item>
  </el-sub-menu>
  <el-sub-menu index="/content_community">
    <template #title>
      <el-icon><MapLocation /></el-icon>
      <span>逛逛社区</span>
    </template>
    <el-menu-item index="/content_community_topic">
      <el-icon><Goods /></el-icon>
      <span>社区话题</span>
    </el-menu-item>
    <el-sub-menu index="/content_community_content">
      <template #title>
        <el-icon><Goods /></el-icon>
        <span>社区内容</span>
      </template>
    </el-sub-menu>
    <el-menu-item index="/content_community_comment">
      <el-icon><Location /></el-icon>
      <span>社区评论</span>
    </el-menu-item>
    <el-menu-item index="/content_community_setting">
      <el-icon><Setting /></el-icon>
      <span>社区设置</span>
    </el-menu-item>
  </el-sub-menu>
  <el-sub-menu index="/content_cms">
    <template #title>
      <el-icon><Guide /></el-icon>
      <span>内容资讯</span>
    </template>
    <el-menu-item index="/content_article_category_index">
      <el-icon><Document /></el-icon>
      <span>文章分类</span>
    </el-menu-item>
    <el-menu-item index="/content_article_index">
      <el-icon><Document /></el-icon>
      <span>文章列表</span>
    </el-menu-item>
  </el-sub-menu>
  <el-sub-menu index="/kefu">
    <template #title>
      <el-icon><Goods /></el-icon>
      <span>客服管理</span>
    </template>
    <el-menu-item index="/setting_store_service_index">
      <el-icon><Camera /></el-icon>
      <span>客服列表</span>
    </el-menu-item>
    <el-menu-item index="/setting_store_service_speechcraft">
      <el-icon><Document /></el-icon>
      <span>客服话术</span>
    </el-menu-item>
    <el-menu-item index="/setting_store_service_feedback">
      <el-icon><User /></el-icon>
      <span>用户留言</span>
    </el-menu-item>
    <el-menu-item index="/kefu_setup">
      <el-icon><Setting /></el-icon>
      <span>客服设置</span>
    </el-menu-item>
  </el-sub-menu>
          </template>
          <template v-if="activeTopMenu === '渠道'">
  <el-sub-menu index="/supplier">
    <template #title>
      <el-icon><Present /></el-icon>
      <span>供应商</span>
    </template>
    <el-menu-item index="/supplier_menu_list">
      <el-icon><Message /></el-icon>
      <span>供应商列表</span>
    </el-menu-item>
    <el-menu-item index="/supplier_apply">
      <el-icon><Discount /></el-icon>
      <span>供应商申请</span>
    </el-menu-item>
    <el-menu-item index="/supplier_orderList_index">
      <el-icon><List /></el-icon>
      <span>订单列表</span>
    </el-menu-item>
    <el-menu-item index="/supplier_afterOrder_index">
      <el-icon><List /></el-icon>
      <span>售后订单</span>
    </el-menu-item>
    <el-menu-item index="/supplier_orderStatistics_index">
      <el-icon><List /></el-icon>
      <span>订单统计</span>
    </el-menu-item>
    <el-menu-item index="/supplier_supplier_index">
      <el-icon><Setting /></el-icon>
      <span>菜单设置</span>
    </el-menu-item>
    <el-menu-item index="/supplier_setting">
      <el-icon><Setting /></el-icon>
      <span>供应商设置</span>
    </el-menu-item>
  </el-sub-menu>
  <el-sub-menu index="/user_channelMerchant">
    <template #title>
      <el-icon><Guide /></el-icon>
      <span>采购商</span>
    </template>
    <el-menu-item index="/user_channelMerchant_examine">
      <el-icon><Phone /></el-icon>
      <span>采购商审核</span>
    </el-menu-item>
    <el-menu-item index="/user_channelMerchant_list">
      <el-icon><DataLine /></el-icon>
      <span>采购商列表</span>
    </el-menu-item>
    <el-menu-item index="/user_channelMerchant_identity">
      <el-icon><Guide /></el-icon>
      <span>采购商身份</span>
    </el-menu-item>
    <el-menu-item index="/user_channelMerchant_setting">
      <el-icon><Setting /></el-icon>
      <span>采购商设置</span>
    </el-menu-item>
  </el-sub-menu>
          </template>
          <template v-if="activeTopMenu === '财务'">
  <el-sub-menu index="/finance_user_extract">
    <template #title>
      <el-icon><Money /></el-icon>
      <span>财务操作</span>
    </template>
    <el-menu-item index="/order_invoice_list">
      <el-icon><MapLocation /></el-icon>
      <span>发票列表</span>
    </el-menu-item>
    <el-menu-item index="/order_invoice_setup">
      <el-icon><Setting /></el-icon>
      <span>发票设置</span>
    </el-menu-item>
  </el-sub-menu>
  <el-sub-menu index="/finance_user_extract_index">
    <template #title>
      <el-icon><Share /></el-icon>
      <span>分销财务</span>
    </template>
    <el-menu-item index="/finance_user_extract_index">
      <el-icon><Present /></el-icon>
      <span>提现申请</span>
    </el-menu-item>
    <el-menu-item index="/setting_system_config_advance">
      <el-icon><Setting /></el-icon>
      <span>提现设置</span>
    </el-menu-item>
  </el-sub-menu>
  <el-sub-menu index="/supplier_finance">
    <template #title>
      <el-icon><Money /></el-icon>
      <span>供应商财务</span>
    </template>
    <el-menu-item index="/supplier_capital_index">
      <el-icon><Money /></el-icon>
      <span>资金流水</span>
    </el-menu-item>
    <el-menu-item index="/supplier_bill_index">
      <el-icon><Box /></el-icon>
      <span>账单记录</span>
    </el-menu-item>
    <el-menu-item index="/supplier_cash_index">
      <el-icon><Present /></el-icon>
      <span>转账申请</span>
    </el-menu-item>
    <el-menu-item index="/supplier_bill_index_1">
      <el-icon><Postcard /></el-icon>
      <span>对账管理</span>
    </el-menu-item>
    <el-menu-item index="/supplier_finance_set">
      <el-icon><Setting /></el-icon>
      <span>财务设置</span>
    </el-menu-item>
  </el-sub-menu>
  <el-sub-menu index="/finance_user_recharge">
    <template #title>
      <el-icon><Money /></el-icon>
      <span>财务记录</span>
    </template>
    <el-menu-item index="/finance_user_recharge_index">
      <el-icon><Present /></el-icon>
      <span>充值记录</span>
    </el-menu-item>
    <el-menu-item index="/statistic_capital">
      <el-icon><Money /></el-icon>
      <span>资金流水</span>
    </el-menu-item>
  </el-sub-menu>
          </template>
          <template v-if="activeTopMenu === '应用端'">
  <el-sub-menu index="/app_wechat">
    <template #title>
      <el-icon><Message /></el-icon>
      <span>公众号</span>
    </template>
    <el-menu-item index="/app_wechat_base">
      <el-icon><Setting /></el-icon>
      <span>基础配置</span>
    </el-menu-item>
    <el-menu-item index="/app_wechat_setting_menus_index">
      <el-icon><Medal /></el-icon>
      <span>微信菜单</span>
    </el-menu-item>
    <el-menu-item index="/app_wechat_card">
      <el-icon><Connection /></el-icon>
      <span>微信会员卡</span>
    </el-menu-item>
    <el-menu-item index="/app_wechat_reply">
      <el-icon><Present /></el-icon>
      <span>自动回复</span>
    </el-menu-item>
    <el-sub-menu index="/app_wechat_news_category_index">
      <template #title>
        <el-icon><DataAnalysis /></el-icon>
        <span>图文管理</span>
      </template>
    </el-sub-menu>
  </el-sub-menu>
  <el-sub-menu index="/app_routine_download">
    <template #title>
      <el-icon><HomeFilled /></el-icon>
      <span>小程序</span>
    </template>
    <el-menu-item index="/app_routine_download">
      <el-icon><Setting /></el-icon>
      <span>小程序配置</span>
    </el-menu-item>
    <el-sub-menu index="/content_live_live_room">
      <template #title>
        <el-icon><Bell /></el-icon>
        <span>直播间管理</span>
      </template>
    </el-sub-menu>
    <el-sub-menu index="/content_live_live_goods">
      <template #title>
        <el-icon><Goods /></el-icon>
        <span>商品管理</span>
      </template>
    </el-sub-menu>
    <el-menu-item index="/content_live_anchor">
      <el-icon><Monitor /></el-icon>
      <span>主播管理</span>
    </el-menu-item>
  </el-sub-menu>
  <el-sub-menu index="/app_pc">
    <template #title>
      <el-icon><Document /></el-icon>
      <span>PC 端</span>
    </template>
    <el-menu-item index="/app_pc">
      <el-icon><Setting /></el-icon>
      <span>PC 配置</span>
    </el-menu-item>
    <el-menu-item index="/setting_pc_group_data">
      <el-icon><VideoCamera /></el-icon>
      <span>PC商城</span>
    </el-menu-item>
  </el-sub-menu>
  <el-sub-menu index="/work_config">
    <template #title>
      <el-icon><Position /></el-icon>
      <span>企业微信</span>
    </template>
    <el-menu-item index="/work_config">
      <el-icon><Setting /></el-icon>
      <span>企微设置</span>
    </el-menu-item>
  </el-sub-menu>
          </template>
          <template v-if="activeTopMenu === '设置'">
  <el-sub-menu index="/setting_base">
    <template #title>
      <el-icon><Setting /></el-icon>
      <span>系统设置</span>
    </template>
    <el-menu-item index="/setting_shop_base">
      <el-icon><Setting /></el-icon>
      <span>系统设置</span>
    </el-menu-item>
    <el-sub-menu index="/setting_notification_index">
      <template #title>
        <el-icon><Setting /></el-icon>
        <span>消息设置</span>
      </template>
      <el-menu-item index="/setting_notification_notificationEdit">
        <el-icon><Setting /></el-icon>
        <span>消息设置</span>
      </el-menu-item>
    </el-sub-menu>
  </el-sub-menu>
  <el-sub-menu index="/setting_service">
    <template #title>
      <el-icon><Setting /></el-icon>
      <span>服务设置</span>
    </template>
    <el-menu-item index="/setting_sms_sms_config_index">
      <el-icon><Trophy /></el-icon>
      <span>一号通管理</span>
    </el-menu-item>
    <el-menu-item index="/setting_system_config_sms">
      <el-icon><Setting /></el-icon>
      <span>一号通配置</span>
    </el-menu-item>
    <el-menu-item index="/setting_third_party">
      <el-icon><Setting /></el-icon>
      <span>接口设置</span>
    </el-menu-item>
    <el-menu-item index="/setting_document">
      <el-icon><PriceTag /></el-icon>
      <span>小票打印</span>
    </el-menu-item>
    <el-menu-item index="/setting_shop_pay">
      <el-icon><Setting /></el-icon>
      <span>支付设置</span>
    </el-menu-item>
    <el-menu-item index="/setting_storage">
      <el-icon><Setting /></el-icon>
      <span>存储配置</span>
    </el-menu-item>
    <el-menu-item index="/setting_document_content">
      <el-icon><PriceTag /></el-icon>
      <span>小票打印</span>
    </el-menu-item>
  </el-sub-menu>
  <el-sub-menu index="/setting_auth_list">
    <template #title>
      <el-icon><Setting /></el-icon>
      <span>权限设置</span>
    </template>
    <el-menu-item index="/setting_system_role_index">
      <el-icon><CreditCard /></el-icon>
      <span>角色管理</span>
    </el-menu-item>
    <el-menu-item index="/setting_system_admin_index">
      <el-icon><Star /></el-icon>
      <span>管理员列表</span>
    </el-menu-item>
    <el-menu-item index="/setting_system_menus_index">
      <el-icon><Menu /></el-icon>
      <span>权限规则</span>
    </el-menu-item>
  </el-sub-menu>
  <el-sub-menu index="/system_config">
    <template #title>
      <el-icon><Setting /></el-icon>
      <span>开发配置</span>
    </template>
    <el-sub-menu index="/system_crontab">
      <template #title>
        <el-icon><ChatDotRound /></el-icon>
        <span>定时任务</span>
      </template>
    </el-sub-menu>
    <el-menu-item index="/system_config_system_config_tab_index">
      <el-icon><Setting /></el-icon>
      <span>配置分类</span>
    </el-menu-item>
    <el-menu-item index="/system_config_system_group_index">
      <el-icon><Setting /></el-icon>
      <span>组合数据</span>
    </el-menu-item>
    <el-menu-item index="/system_config_system_config_tab_list">
      <el-icon><Setting /></el-icon>
      <span>配置列表</span>
    </el-menu-item>
    <el-menu-item index="/system_config_system_group_list">
      <el-icon><Document /></el-icon>
      <span>组合数据列表</span>
    </el-menu-item>
    <el-menu-item index="/out">
      <el-icon><PriceTag /></el-icon>
      <span>对外接口</span>
    </el-menu-item>
    <el-menu-item index="/out_interface">
      <el-icon><MapLocation /></el-icon>
      <span>接口文档</span>
    </el-menu-item>
  </el-sub-menu>
  <el-sub-menu index="/system_maintain">
    <template #title>
      <el-icon><CreditCard /></el-icon>
      <span>安全维护</span>
    </template>
    <el-menu-item index="/system_maintain_clear_index">
      <el-icon><Menu /></el-icon>
      <span>刷新缓存</span>
    </el-menu-item>
    <el-menu-item index="/system_maintain_system_log_index">
      <el-icon><Trophy /></el-icon>
      <span>系统日志</span>
    </el-menu-item>
    <el-menu-item index="/system_maintain_system_file_index">
      <el-icon><Message /></el-icon>
      <span>文件校验</span>
    </el-menu-item>
    <el-menu-item index="/system_maintain_system_cleardata_index">
      <el-icon><HomeFilled /></el-icon>
      <span>清除数据</span>
    </el-menu-item>
    <el-menu-item index="/system_maintain_system_databackup_index">
      <el-icon><Location /></el-icon>
      <span>数据备份</span>
    </el-menu-item>
    <el-menu-item index="/system_log">
      <el-icon><Trophy /></el-icon>
      <span>系统日志</span>
    </el-menu-item>
  </el-sub-menu>
  <el-menu-item index="/system_user">
    <el-icon><Headset /></el-icon>
    <span>个人中心</span>
  </el-menu-item>
          </template>

        </el-menu>
      </el-aside>

      <!-- Content Area -->
      <el-main class="content-area">
        
        <div class="tags-view-container">
          <el-tabs
            v-model="activeTab"
            type="card"
            closable
            @tab-click="handleTabClick"
            @tab-remove="handleTabRemove"
          >
            <el-tab-pane
              v-for="item in visitedViews"
              :key="item.path"
              :label="item.title"
              :name="item.path"
            />
          </el-tabs>
        </div>
        <div class="page-container">

          <router-view v-slot="{ Component }">
            <transition name="fade" mode="out-in">
              <component :is="Component" />
            </transition>
          </router-view>
        </div>
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Search, FullScreen, Bell, ArrowLeft, ArrowRight, ArrowDown, SwitchButton, RefreshRight, Fold, Expand, Menu, User, Star, Goods, List, Setting, DataLine, DataAnalysis, Message, ChatDotRound, Location, Picture, Camera, VideoCamera, Headset, Phone, More, Share, Ticket, Money, Coin, Wallet, Discount, PriceTag, Guide, Position, Connection, Link, Monitor, Cpu, Collection, Folder, Document, Files, Box, OfficeBuilding, School, House, Shop, ShoppingCart, ShoppingCartFull, Sell, SoldOut, Present, Medal, Trophy, Reading, Notebook, MapLocation, Grid, HomeFilled, Management, Histogram, TrendCharts, Briefcase, Postcard, CreditCard } from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()

const scrollContainer = ref(null)
const showScrollArrows = ref(false)

const checkScroll = () => {
  if (scrollContainer.value) {
    const el = scrollContainer.value
    showScrollArrows.value = el.scrollWidth > el.clientWidth
  }
}

const scrollMenu = (direction) => {
  if (scrollContainer.value) {
    const el = scrollContainer.value
    const amount = 200
    el.scrollBy({ left: direction === 'left' ? -amount : amount, behavior: 'smooth' })
  }
}

onMounted(() => {
  checkScroll()
  window.addEventListener('resize', checkScroll)
})

onUnmounted(() => {
  window.removeEventListener('resize', checkScroll)
})

const isCollapse = ref(false)

const topMenus = [
  { name: '商城' }, { name: '用户' }, { name: '营销' }, { name: '分销' },
  { name: '店铺' }, { name: '渠道' }, { name: '财务' }, { name: '设置' }
]
const activeTopMenu = ref('商城')

const sideMenuHtml = ref('')


const routeMetaMap = {
  "/_dashboard": {
    "title": "首页",
    "topMenu": "商城"
  },
  "/_home_": {
    "title": "首页",
    "topMenu": "商城"
  },
  "/_product": {
    "title": "商品",
    "topMenu": "商城"
  },
  "/_product_product_list": {
    "title": "商品列表",
    "topMenu": "商城"
  },
  "/_product_product": {
    "title": "产品列表",
    "topMenu": "商城"
  },
  "/_adminproduct_product_type_header": {
    "title": "商品列表头部",
    "topMenu": "商城"
  },
  "/_admin*": {
    "title": "附加权限",
    "topMenu": "设置"
  },
  "/_adminproduct_set_show_<id>_<is_show>": {
    "title": "产品状态",
    "topMenu": "商城"
  },
  "/_adminproduct_product_set_product_<id>": {
    "title": "快速编辑",
    "topMenu": "商城"
  },
  "/_adminproduct_product_product_show": {
    "title": "批量上架商品",
    "topMenu": "商城"
  },
  "/_adminproduct_crawl": {
    "title": "采集商品",
    "topMenu": "商城"
  },
  "/_adminproduct_crawl_save": {
    "title": "采集商品保存",
    "topMenu": "商城"
  },
  "/_adminproduct_product_list": {
    "title": "商品列表插件",
    "topMenu": "商城"
  },
  "/product_product_product_show": {
    "title": "批量设置",
    "topMenu": "商城"
  },
  "/_product_product_classify": {
    "title": "商品分类",
    "topMenu": "商城"
  },
  "/_adminproduct_category": {
    "title": "新增分类",
    "topMenu": "商城"
  },
  "/_admincategory_tree_:type": {
    "title": "分类树形列表",
    "topMenu": "商城"
  },
  "/_adminproduct_category_<id>": {
    "title": "修改分类",
    "topMenu": "商城"
  },
  "/_adminproduct_category_set_show_<id>_<is_show>": {
    "title": "分类状态",
    "topMenu": "商城"
  },
  "/_adminproduct_category_set_category_<id>": {
    "title": "快速编辑",
    "topMenu": "商城"
  },
  "/_admincategory_create": {
    "title": "分类表单添加",
    "topMenu": "商城"
  },
  "/_admincategory_<id>_edit": {
    "title": "分类表单编辑",
    "topMenu": "商城"
  },
  "/_product_add_product": {
    "title": "产品添加",
    "topMenu": "商城"
  },
  "/_product_save": {
    "title": "添加产品保存",
    "topMenu": "商城"
  },
  "/_adminproduct_product_get_rule": {
    "title": "获取属性模板列表",
    "topMenu": "商城"
  },
  "/_adminproduct_product_get_template": {
    "title": "运费模板列表",
    "topMenu": "商城"
  },
  "/_adminproduct_generate_attr_<id>": {
    "title": "生成属性",
    "topMenu": "商城"
  },
  "/_product_product_attr": {
    "title": "商品规格",
    "topMenu": "商城"
  },
  "/_adminproduct_product_rule": {
    "title": "属性规则列表",
    "topMenu": "商城"
  },
  "/_adminproduct_rule_<id>": {
    "title": "保存修改规则",
    "topMenu": "商城"
  },
  "/_adminproduct_product_rule_<id>": {
    "title": "规则详情",
    "topMenu": "商城"
  },
  "/_adminproduct_product_rule_delete": {
    "title": "删除规则",
    "topMenu": "商城"
  },
  "/_product_label": {
    "title": "商品标签",
    "topMenu": "商城"
  },
  "/_product_product_brand": {
    "title": "商品品牌",
    "topMenu": "商城"
  },
  "/_product_unitList": {
    "title": "商品单位",
    "topMenu": "商城"
  },
  "/_product_specs": {
    "title": "商品参数",
    "topMenu": "商城"
  },
  "/_product_ensure": {
    "title": "保障服务",
    "topMenu": "商城"
  },
  "/_product_ensure_create": {
    "title": "添加商品参数模版",
    "topMenu": "商城"
  },
  "/_setting_system_form": {
    "title": "系统表单",
    "topMenu": "商城"
  },
  "/_setting_system_create": {
    "title": "添加系统表单",
    "topMenu": "商城"
  },
  "/_setting_system_form_data": {
    "title": "系统表单收集数据",
    "topMenu": "商城"
  },
  "/_product_product_reply": {
    "title": "商品评论",
    "topMenu": "商城"
  },
  "/_adminproduct_reply": {
    "title": "评论列表",
    "topMenu": "商城"
  },
  "/_adminproduct_reply_fictitious_reply": {
    "title": "虚拟评论表单",
    "topMenu": "商城"
  },
  "/_adminproduct_reply_save_fictitious_reply": {
    "title": "保存虚拟评论",
    "topMenu": "商城"
  },
  "/_adminproduct_reply_<id>": {
    "title": "删除评论",
    "topMenu": "商城"
  },
  "/_adminreply_set_reply_<id>": {
    "title": "评论回复",
    "topMenu": "商城"
  },
  "/_product_product_reply_config": {
    "title": "评论设置",
    "topMenu": "商城"
  },
  "/_order": {
    "title": "订单",
    "topMenu": "商城"
  },
  "/_order_list": {
    "title": "订单列表",
    "topMenu": "商城"
  },
  "/_adminorder_list": {
    "title": "订单列表",
    "topMenu": "商城"
  },
  "/_adminorder_chart": {
    "title": "订单数据",
    "topMenu": "商城"
  },
  "/_adminorder_write": {
    "title": "订单核销",
    "topMenu": "商城"
  },
  "/_adminorder_take_<id>": {
    "title": "订单收货",
    "topMenu": "商城"
  },
  "/_adminorder_express_<id>": {
    "title": "订单物流信息",
    "topMenu": "商城"
  },
  "/_adminorder_delivery": {
    "title": "发货",
    "topMenu": "商城"
  },
  "/_adminorder_delivery_<id>": {
    "title": "订单发货",
    "topMenu": "商城"
  },
  "/_adminorder_express_list": {
    "title": "物流公司列表",
    "topMenu": "商城"
  },
  "/_adminorder_distribution": {
    "title": "订单配送",
    "topMenu": "商城"
  },
  "/_adminorder_distribution_<id>": {
    "title": "修改配送信息",
    "topMenu": "商城"
  },
  "/_adminorder_refund": {
    "title": "退款",
    "topMenu": "商城"
  },
  "/_adminorder_refund_<id>": {
    "title": "订单退款",
    "topMenu": "商城"
  },
  "/_adminorder_update": {
    "title": "修改",
    "topMenu": "商城"
  },
  "/_adminorder_edit_<id>": {
    "title": "订单修改表格",
    "topMenu": "商城"
  },
  "/_adminorder_update_<id>": {
    "title": "订单修改",
    "topMenu": "商城"
  },
  "/_adminorder_no_refund": {
    "title": "不退款",
    "topMenu": "商城"
  },
  "/_adminorder_no_refund_<id>": {
    "title": "不退款理由修改",
    "topMenu": "商城"
  },
  "/_adminorder_refund_integral": {
    "title": "退积分",
    "topMenu": "商城"
  },
  "/order_dels": {
    "title": "订单号核销",
    "topMenu": "商城"
  },
  "/_order_split_delivery": {
    "title": "拆单发货",
    "topMenu": "商城"
  },
  "/queue_stop_wrong_queue_<id>": {
    "title": "停止任务",
    "topMenu": "商城"
  },
  "/_order_split_list": {
    "title": "子订单列表",
    "topMenu": "商城"
  },
  "/_order_refund": {
    "title": "售后订单",
    "topMenu": "商城"
  },
  "/_setting_distribution_deliver": {
    "title": "发货设置",
    "topMenu": "商城"
  },
  "/_setting_freight_shipping_templates_list": {
    "title": "运费模板",
    "topMenu": "商城"
  },
  "/_setting_freight_express_index": {
    "title": "物流公司",
    "topMenu": "商城"
  },
  "/_setting_delivery_service_index": {
    "title": "配送员管理",
    "topMenu": "商城"
  },
  "/_setting_delivery_service_edit": {
    "title": "编辑配送员",
    "topMenu": "商城"
  },
  "/_setting_delivery_service_add": {
    "title": "添加配送员",
    "topMenu": "商城"
  },
  "/_setting_shop_storeList": {
    "title": "自提点列表",
    "topMenu": "商城"
  },
  "/_setting_city_delivery_setting": {
    "title": "配送设置",
    "topMenu": "商城"
  },
  "/_setting_city_delivery_record": {
    "title": "配送记录",
    "topMenu": "商城"
  },
  "/_setting_freight_city_list": {
    "title": "城市数据",
    "topMenu": "商城"
  },
  "/_setting_shop": {
    "title": "商城设置",
    "topMenu": "商城"
  },
  "/_setting_shop_product": {
    "title": "商品设置",
    "topMenu": "商城"
  },
  "/_setting_shop_trade": {
    "title": "交易设置",
    "topMenu": "商城"
  },
  "/_setting_city_delivery": {
    "title": "同城配送",
    "topMenu": "商城"
  },
  "/_setting_shop_distribution": {
    "title": "配送设置",
    "topMenu": "商城"
  },
  "/_setting_shop_agreemant": {
    "title": "政策协议",
    "topMenu": "商城"
  },
  "/_setting_shop_releaseset": {
    "title": "释放比例设置",
    "topMenu": "商城"
  },
  "/_setting_shop_coinoffset": {
    "title": "屏蔽前端代币设置",
    "topMenu": "商城"
  },
  "/_statistic_user": {
    "title": "用户概况",
    "topMenu": "用户"
  },
  "/_user_manage": {
    "title": "用户",
    "topMenu": "用户"
  },
  "/_user_list": {
    "title": "用户列表",
    "topMenu": "用户"
  },
  "/_user_coupon": {
    "title": "发送优惠卷",
    "topMenu": "用户"
  },
  "/_wechat_news_": {
    "title": "发送图文",
    "topMenu": "用户"
  },
  "/_user_group_set_": {
    "title": "批量用户分组",
    "topMenu": "用户"
  },
  "/_user_set_label": {
    "title": "批量设置标签",
    "topMenu": "用户"
  },
  "/_user_edit_other": {
    "title": "积分余额",
    "topMenu": "用户"
  },
  "/_user_user_level": {
    "title": "等级任务",
    "topMenu": "用户"
  },
  "/_user_save": {
    "title": "添加用户",
    "topMenu": "用户"
  },
  "/_user_group": {
    "title": "添加修改用户分组",
    "topMenu": "用户"
  },
  "/_user_label": {
    "title": "用户标签",
    "topMenu": "用户"
  },
  "/_user_label_create": {
    "title": "添加标签",
    "topMenu": "用户"
  },
  "/_user_label_add": {
    "title": "添加修改用户标签",
    "topMenu": "用户"
  },
  "/_user_label_cate": {
    "title": "标签分类",
    "topMenu": "用户"
  },
  "/_user_label_cate_add": {
    "title": "添加标签分类",
    "topMenu": "用户"
  },
  "/_user_label_cate_edit": {
    "title": "修改标签分类",
    "topMenu": "用户"
  },
  "/user_user_label_cate_<id>_edit": {
    "title": "获取修改标签分类表单",
    "topMenu": "用户"
  },
  "/_marketing_channel_code": {
    "title": "渠道码",
    "topMenu": "用户"
  },
  "/_marketing_channel_code_create": {
    "title": "添加渠道码",
    "topMenu": "用户"
  },
  "/_user_userSet": {
    "title": "用户设置",
    "topMenu": "用户"
  },
  "/_user": {
    "title": "用户运营",
    "topMenu": "用户"
  },
  "/_vipuser_level_list": {
    "title": "用户等级",
    "topMenu": "用户"
  },
  "/_user_level_add": {
    "title": "添加修改用户等级",
    "topMenu": "用户"
  },
  "/_user_levelSet": {
    "title": "等级设置",
    "topMenu": "用户"
  },
  "/_user_registerSet": {
    "title": "新人礼包",
    "topMenu": "用户"
  },
  "/_user_memberGift": {
    "title": "激活有礼",
    "topMenu": "用户"
  },
  "/_marketing_store_coupon": {
    "title": "优惠券",
    "topMenu": "营销"
  },
  "/_marketing_store_coupon_issue_index": {
    "title": "优惠券列表",
    "topMenu": "用户"
  },
  "/_marketing_store_coupon_issue_create": {
    "title": "添加优惠卷",
    "topMenu": "用户"
  },
  "/marketing_coupon_copy_369": {
    "title": "复制优惠券",
    "topMenu": "用户"
  },
  "/_marketing_store_coupon_user_index": {
    "title": "领取记录",
    "topMenu": "用户"
  },
  "/_marketing_integral_system_config_3_11": {
    "title": "积分配置",
    "topMenu": "用户"
  },
  "/_marketing_integral_system_config": {
    "title": "积分配置",
    "topMenu": "用户"
  },
  "/_marketing_user_point_index": {
    "title": "积分日志",
    "topMenu": "用户"
  },
  "/_marketing_balance_recharge": {
    "title": "代币金额",
    "topMenu": "用户"
  },
  "/_marketing_setup_recharge": {
    "title": "代币设置",
    "topMenu": "用户"
  },
  "/integral_release_index": {
    "title": "积分释放配置",
    "topMenu": "用户"
  },
  "/_marketing_weather_tpapply": {
    "title": "代币审核列表",
    "topMenu": "用户"
  },
  "/_marketing_weather_tongpiao": {
    "title": "用户账单",
    "topMenu": "用户"
  },
  "/_work": {
    "title": "企业微信",
    "topMenu": "用户"
  },
  "/_work_client_list": {
    "title": "客户列表",
    "topMenu": "用户"
  },
  "/_work_channel_code": {
    "title": "企微渠道码",
    "topMenu": "用户"
  },
  "/_work_welcome": {
    "title": "欢迎语",
    "topMenu": "用户"
  },
  "/_work_createCode": {
    "title": "添加企业渠道码",
    "topMenu": "用户"
  },
  "/_work_addWelcome": {
    "title": "新建好友欢迎语",
    "topMenu": "用户"
  },
  "/_work_client_group": {
    "title": "客户群发",
    "topMenu": "用户"
  },
  "/_work_client_add_group": {
    "title": "添加客户群发",
    "topMenu": "用户"
  },
  "/_work_client_add_moment": {
    "title": "朋友圈添加",
    "topMenu": "用户"
  },
  "/_work_client_moment": {
    "title": "朋友圈列表",
    "topMenu": "用户"
  },
  "/_work_client_group_info": {
    "title": "客户群发详情",
    "topMenu": "用户"
  },
  "/_work_client_moment_info": {
    "title": "朋友圈详情",
    "topMenu": "用户"
  },
  "/_work_client_group_chat": {
    "title": "客户群列表",
    "topMenu": "用户"
  },
  "/_work_auth_group": {
    "title": "自动拉群",
    "topMenu": "用户"
  },
  "/_work_addAuthGroup": {
    "title": "新建自动拉群",
    "topMenu": "用户"
  },
  "/_work_client_statistical": {
    "title": "客户群统计",
    "topMenu": "用户"
  },
  "/_work_group_template": {
    "title": "客户群群发",
    "topMenu": "用户"
  },
  "/_work_group_add_template": {
    "title": "添加客户群群发",
    "topMenu": "用户"
  },
  "/_work_group_template_info": {
    "title": "客户群群发详情",
    "topMenu": "用户"
  },
  "/_work_staffList": {
    "title": "员工列表",
    "topMenu": "用户"
  },
  "/_user_importRecord": {
    "title": "用户导入记录",
    "topMenu": "用户"
  },
  "/_marketing_home": {
    "title": "营销中心",
    "topMenu": "营销"
  },
  "/_vipuser_grade": {
    "title": "付费会员",
    "topMenu": "营销"
  },
  "/_vipuser_grade_type": {
    "title": "会员类型",
    "topMenu": "营销"
  },
  "/_vipuser_grade_right": {
    "title": "会员权益",
    "topMenu": "营销"
  },
  "/_vipuser_grade_agreement": {
    "title": "会员协议",
    "topMenu": "营销"
  },
  "/_vipuser_grade_card": {
    "title": "卡密会员",
    "topMenu": "营销"
  },
  "/_vipuser_grade_record": {
    "title": "会员记录",
    "topMenu": "营销"
  },
  "/_vipuser_grade_list": {
    "title": "会员卡列表",
    "topMenu": "营销"
  },
  "/_user_svipSet": {
    "title": "会员设置",
    "topMenu": "营销"
  },
  "/_marketing_store_coupon_index": {
    "title": "优惠券模板",
    "topMenu": "营销"
  },
  "/_marketing_store_coupon_add": {
    "title": "添加优惠卷",
    "topMenu": "营销"
  },
  "/_marketing_store_coupon_push": {
    "title": "发布优惠卷",
    "topMenu": "营销"
  },
  "/_marketing_lottery_index": {
    "title": "抽奖",
    "topMenu": "营销"
  },
  "/_marketing_lottery_list": {
    "title": "抽奖列表",
    "topMenu": "营销"
  },
  "/_marketing_lottery_create": {
    "title": "抽奖配置",
    "topMenu": "营销"
  },
  "/_marketing_lottery_recording_list": {
    "title": "中奖记录",
    "topMenu": "营销"
  },
  "/_marketing_lottery_config": {
    "title": "抽奖配置",
    "topMenu": "营销"
  },
  "/_marketing_store_combination": {
    "title": "拼团",
    "topMenu": "营销"
  },
  "/_marketing_store_combination_index": {
    "title": "拼团商品",
    "topMenu": "营销"
  },
  "/_marketing_store_combination_combina_list": {
    "title": "拼团列表",
    "topMenu": "营销"
  },
  "/_marketing_store_combination_create": {
    "title": "添加拼团",
    "topMenu": "营销"
  },
  "/_marketing_store_combination_statistics": {
    "title": "拼团统计",
    "topMenu": "营销"
  },
  "/_marketing_store_seckill": {
    "title": "秒杀",
    "topMenu": "营销"
  },
  "/_marketing_store_seckill_list": {
    "title": "秒杀列表",
    "topMenu": "营销"
  },
  "/_marketing_store_seckill_index": {
    "title": "秒杀商品",
    "topMenu": "营销"
  },
  "/_marketing_store_seckill_statistics": {
    "title": "秒杀统计",
    "topMenu": "营销"
  },
  "/_marketing_store_seckill_create": {
    "title": "添加秒杀",
    "topMenu": "营销"
  },
  "/_marketing_store_seckill_data_index": {
    "title": "秒杀配置",
    "topMenu": "营销"
  },
  "/_marketing_store_bargain": {
    "title": "砍价",
    "topMenu": "营销"
  },
  "/_marketing_store_bargain_index": {
    "title": "砍价商品",
    "topMenu": "营销"
  },
  "/_marketing_store_bargain_attr": {
    "title": "附加权限",
    "topMenu": "营销"
  },
  "/_marketing_store_bargain_public": {
    "title": "公共权限",
    "topMenu": "营销"
  },
  "/_marketing_store_bargain_create": {
    "title": "添加砍价",
    "topMenu": "营销"
  },
  "/_marketing_store_bargain_bargain_list": {
    "title": "砍价列表",
    "topMenu": "营销"
  },
  "/_marketing_store_bargain_setting": {
    "title": "砍价设置",
    "topMenu": "营销"
  },
  "/_marketing_store_bargain_statistics": {
    "title": "砍价统计",
    "topMenu": "营销"
  },
  "/_marketing_giftCard": {
    "title": "礼品卡",
    "topMenu": "营销"
  },
  "/_marketing_giftCard_manage": {
    "title": "生成卡号",
    "topMenu": "营销"
  },
  "/_marketing_giftCard_index": {
    "title": "礼品卡列表",
    "topMenu": "营销"
  },
  "/_marketing_giftCard_record": {
    "title": "卡密管理",
    "topMenu": "营销"
  },
  "/_marketing_giftCard_create": {
    "title": "添加礼品卡",
    "topMenu": "营销"
  },
  "/_sysytem_automation": {
    "title": "自动化运营",
    "topMenu": "营销"
  },
  "/_marketing_automation": {
    "title": "智能推送",
    "topMenu": "营销"
  },
  "/_marketing_automation_create": {
    "title": "创建定时任务",
    "topMenu": "营销"
  },
  "/_marketing_birthday": {
    "title": "生日有礼",
    "topMenu": "营销"
  },
  "/_marketing_discount": {
    "title": "促销",
    "topMenu": "营销"
  },
  "/_marketing_discount_list": {
    "title": "限时折扣",
    "topMenu": "营销"
  },
  "/_marketing_discount_add": {
    "title": "添加限时折扣",
    "topMenu": "营销"
  },
  "/_marketing_discount_full_discount": {
    "title": "满减满折",
    "topMenu": "营销"
  },
  "/_marketing_discount_add_discount": {
    "title": "添加满减满折",
    "topMenu": "营销"
  },
  "/_marketing_discount_give": {
    "title": "满送活动",
    "topMenu": "营销"
  },
  "/_marketing_discount_add_give": {
    "title": "添加满减送",
    "topMenu": "营销"
  },
  "/_marketing_discount_pieces_discount": {
    "title": "第N件N折",
    "topMenu": "营销"
  },
  "/_marketing_discount_add_pieces": {
    "title": "添加第N件N折",
    "topMenu": "营销"
  },
  "/_marketing_store_discounts_index": {
    "title": "组合套餐",
    "topMenu": "营销"
  },
  "/_marketing_store_discounts_create": {
    "title": "添加、编辑优惠套餐",
    "topMenu": "营销"
  },
  "/_marketing_user_point": {
    "title": "积分",
    "topMenu": "营销"
  },
  "/_marketing_integral_classify": {
    "title": "积分分类",
    "topMenu": "营销"
  },
  "/_marketing_store_integral_index": {
    "title": "积分商品",
    "topMenu": "营销"
  },
  "/_marketing_store_integral_create": {
    "title": "添加积分商品",
    "topMenu": "营销"
  },
  "/_pages_marketing_store_integral_add_store_integral": {
    "title": "批量添加积分商品",
    "topMenu": "营销"
  },
  "/_marketing_point_statistic": {
    "title": "积分统计",
    "topMenu": "营销"
  },
  "/_marketing_sign": {
    "title": "签到",
    "topMenu": "营销"
  },
  "/_marketing_sign_config": {
    "title": "签到配置",
    "topMenu": "营销"
  },
  "/_marketing_sign_rewards": {
    "title": "签到奖励",
    "topMenu": "营销"
  },
  "/_marketing_activity_background": {
    "title": "活动背景",
    "topMenu": "营销"
  },
  "/_marketing_activity_frame": {
    "title": "活动边框",
    "topMenu": "营销"
  },
  "/_marketing_activity_frame_create": {
    "title": "添加活动边框",
    "topMenu": "营销"
  },
  "/_marketing_activity_background_create": {
    "title": "添加活动背景",
    "topMenu": "营销"
  },
  "/_agent_agent_manage_index": {
    "title": "分销员管理",
    "topMenu": "分销"
  },
  "/_setting_membership_level_index": {
    "title": "分销员等级",
    "topMenu": "分销"
  },
  "/_finance_finance_commission": {
    "title": "佣金记录",
    "topMenu": "分销"
  },
  "/_agent_promoter_apply": {
    "title": "分销员申请",
    "topMenu": "分销"
  },
  "/_setting_system_config_retail_2_9": {
    "title": "分销模式",
    "topMenu": "分销"
  },
  "/_setting_system_config_rake_back": {
    "title": "返佣设置",
    "topMenu": "分销"
  },
  "/_agent_agreement": {
    "title": "分销说明",
    "topMenu": "分销"
  },
  "/_agent_division": {
    "title": "团队分销",
    "topMenu": "分销"
  },
  "/_agent_division_list": {
    "title": "团队列表",
    "topMenu": "分销"
  },
  "/_agent_agent_list": {
    "title": "代理列表",
    "topMenu": "分销"
  },
  "/_agent_apply_list": {
    "title": "代理申请",
    "topMenu": "分销"
  },
  "/_setting_shop_division": {
    "title": "团队配置",
    "topMenu": "分销"
  },
  "/_agent_statistics": {
    "title": "团队统计",
    "topMenu": "分销"
  },
  "/_agent_order": {
    "title": "团队订单",
    "topMenu": "分销"
  },
  "/_setting_pages": {
    "title": "店铺装修",
    "topMenu": "店铺"
  },
  "/_setting_pages_devise": {
    "title": "首页装修",
    "topMenu": "店铺"
  },
  "/_setting_pages_diy": {
    "title": "页面编辑",
    "topMenu": "店铺"
  },
  "/_setting_diy": {
    "title": "附加权限",
    "topMenu": "店铺"
  },
  "/_setting_pages_template": {
    "title": "页面设计",
    "topMenu": "店铺"
  },
  "/_setting_theme_style": {
    "title": "主题风格",
    "topMenu": "店铺"
  },
  "/diy_color_change_:status_:type": {
    "title": "设置主题风格",
    "topMenu": "店铺"
  },
  "/_setting_pages_product_category": {
    "title": "商品分类",
    "topMenu": "店铺"
  },
  "/_setting_pages_home": {
    "title": "个人中心",
    "topMenu": "店铺"
  },
  "/_setting_pages_product_detail": {
    "title": "商品详情",
    "topMenu": "店铺"
  },
  "/_setting_pages_fab": {
    "title": "悬浮菜单",
    "topMenu": "店铺"
  },
  "/_system_file": {
    "title": "素材中心",
    "topMenu": "店铺"
  },
  "/_setting_system_visualization_data": {
    "title": "开屏广告",
    "topMenu": "店铺"
  },
  "/_product_hotWords": {
    "title": "搜索热词",
    "topMenu": "店铺"
  },
  "/_content_community": {
    "title": "逛逛社区",
    "topMenu": "店铺"
  },
  "/_content_community_topic": {
    "title": "社区话题",
    "topMenu": "店铺"
  },
  "/_content_community_content": {
    "title": "社区内容",
    "topMenu": "店铺"
  },
  "/_content_community_addContent": {
    "title": "添加社区内容",
    "topMenu": "店铺"
  },
  "/_content_community_comment": {
    "title": "社区评论",
    "topMenu": "店铺"
  },
  "/_content_community_setting": {
    "title": "社区设置",
    "topMenu": "店铺"
  },
  "/_content_cms": {
    "title": "内容资讯",
    "topMenu": "店铺"
  },
  "/_content_article_category_index": {
    "title": "文章分类",
    "topMenu": "店铺"
  },
  "/_content_article_index": {
    "title": "文章列表",
    "topMenu": "店铺"
  },
  "/_content_article_add_article": {
    "title": "文章添加",
    "topMenu": "店铺"
  },
  "/_kefu": {
    "title": "客服管理",
    "topMenu": "店铺"
  },
  "/_setting_store_service_index": {
    "title": "客服列表",
    "topMenu": "店铺"
  },
  "/_setting_store_service_edit": {
    "title": "编辑客服",
    "topMenu": "店铺"
  },
  "/_setting_store_service_add": {
    "title": "添加客服",
    "topMenu": "店铺"
  },
  "/_setting_store_service_speechcraft": {
    "title": "客服话术",
    "topMenu": "店铺"
  },
  "/*": {
    "title": "附件权限",
    "topMenu": "店铺"
  },
  "/_setting_store_service_speechcraft_add": {
    "title": "添加话术",
    "topMenu": "店铺"
  },
  "/_setting_store_service_speechcraft_edit": {
    "title": "编辑话术",
    "topMenu": "店铺"
  },
  "/_setting_store_service_speechcraft_cate": {
    "title": "话术分类",
    "topMenu": "店铺"
  },
  "/_setting_store_service_speechcraft_cate_create": {
    "title": "添加话术分类",
    "topMenu": "店铺"
  },
  "/_setting_store_service_speechcraft_cate_edit": {
    "title": "修改话术分类",
    "topMenu": "店铺"
  },
  "/app_wechat_speechcraftcate_<id>_edit": {
    "title": "获取话术分类表单",
    "topMenu": "店铺"
  },
  "/_setting_store_service_feedback": {
    "title": "用户留言",
    "topMenu": "店铺"
  },
  "/_kefu_setup": {
    "title": "客服设置",
    "topMenu": "店铺"
  },
  "/_supplier": {
    "title": "供应商",
    "topMenu": "渠道"
  },
  "/_supplier_menu_list": {
    "title": "供应商列表",
    "topMenu": "渠道"
  },
  "/_marketing_channel_code_statistic": {
    "title": "二维码统计",
    "topMenu": "渠道"
  },
  "/_supplier_apply": {
    "title": "供应商申请",
    "topMenu": "渠道"
  },
  "/_supplier_orderList_index": {
    "title": "订单列表",
    "topMenu": "渠道"
  },
  "/_supplier_afterOrder_index": {
    "title": "售后订单",
    "topMenu": "渠道"
  },
  "/_supplier_orderStatistics_index": {
    "title": "订单统计",
    "topMenu": "渠道"
  },
  "/_supplier_supplier_index": {
    "title": "菜单设置",
    "topMenu": "渠道"
  },
  "/_supplier_supplierAdd": {
    "title": "添加供应商",
    "topMenu": "渠道"
  },
  "/_supplier_setting": {
    "title": "供应商设置",
    "topMenu": "渠道"
  },
  "/_user_channelMerchant": {
    "title": "采购商",
    "topMenu": "渠道"
  },
  "/_user_channelMerchant_examine": {
    "title": "采购商审核",
    "topMenu": "渠道"
  },
  "/_user_channelMerchant_list": {
    "title": "采购商列表",
    "topMenu": "渠道"
  },
  "/_user_channelMerchant_identity": {
    "title": "采购商身份",
    "topMenu": "渠道"
  },
  "/_user_channelMerchant_setting": {
    "title": "采购商设置",
    "topMenu": "渠道"
  },
  "/_finance_user_extract": {
    "title": "财务操作",
    "topMenu": "财务"
  },
  "/_order_invoice_list": {
    "title": "发票列表",
    "topMenu": "财务"
  },
  "/_adminorder_info_<id>": {
    "title": "附加权限",
    "topMenu": "财务"
  },
  "/_order_invoice_setup": {
    "title": "发票设置",
    "topMenu": "财务"
  },
  "/_finance_user_extract_index": {
    "title": "提现申请",
    "topMenu": "财务"
  },
  "/_setting_system_config_advance": {
    "title": "提现设置",
    "topMenu": "财务"
  },
  "/_supplier_finance": {
    "title": "供应商财务",
    "topMenu": "财务"
  },
  "/_supplier_capital_index": {
    "title": "资金流水",
    "topMenu": "财务"
  },
  "/_supplier_bill_index": {
    "title": "账单记录",
    "topMenu": "财务"
  },
  "/_supplier_cash_index": {
    "title": "转账申请",
    "topMenu": "财务"
  },
  "/_supplier_bill_index_1": {
    "title": "对账管理",
    "topMenu": "财务"
  },
  "/_supplier_finance_set": {
    "title": "财务设置",
    "topMenu": "财务"
  },
  "/_finance_user_recharge": {
    "title": "财务记录",
    "topMenu": "财务"
  },
  "/_order_offline": {
    "title": "收款记录",
    "topMenu": "财务"
  },
  "/_finance_user_recharge_index": {
    "title": "充值记录",
    "topMenu": "财务"
  },
  "/_finance_finance_bill": {
    "title": "购买记录",
    "topMenu": "财务"
  },
  "/_statistic_capital": {
    "title": "资金流水",
    "topMenu": "财务"
  },
  "/_statistic_product": {
    "title": "商品统计",
    "topMenu": "统计"
  },
  "/_statistic_transaction": {
    "title": "交易统计",
    "topMenu": "统计"
  },
  "/_statistic_order": {
    "title": "订单统计",
    "topMenu": "统计"
  },
  "/_statistic_balance": {
    "title": "余额统计",
    "topMenu": "统计"
  },
  "/_app_wechat": {
    "title": "公众号",
    "topMenu": "应用端"
  },
  "/_app_wechat_base": {
    "title": "基础配置",
    "topMenu": "应用端"
  },
  "/_app_wechat_setting_menus_index": {
    "title": "微信菜单",
    "topMenu": "应用端"
  },
  "/_app_wechat_card": {
    "title": "微信会员卡",
    "topMenu": "应用端"
  },
  "/_app_wechat_reply": {
    "title": "自动回复",
    "topMenu": "应用端"
  },
  "/_app_wechat_reply_follow_subscribe": {
    "title": "微信关注回复",
    "topMenu": "应用端"
  },
  "/_app_wechat_reply_keyword": {
    "title": "关键字回复",
    "topMenu": "应用端"
  },
  "/_app_wechat_reply_index_default": {
    "title": "无效关键词回复",
    "topMenu": "应用端"
  },
  "/_app_wechat_reply_keyword_save": {
    "title": "关键字添加",
    "topMenu": "应用端"
  },
  "/_app_wechat_news_category_index": {
    "title": "图文管理",
    "topMenu": "应用端"
  },
  "/_app_wechat_news_category_save": {
    "title": "图文添加",
    "topMenu": "应用端"
  },
  "/_app_routine_download": {
    "title": "小程序下载",
    "topMenu": "应用端"
  },
  "/_content_live_live_room": {
    "title": "直播间管理",
    "topMenu": "应用端"
  },
  "/_content_live_add_live_room": {
    "title": "添加直播间",
    "topMenu": "应用端"
  },
  "/_*": {
    "title": "附加权限",
    "topMenu": "应用端"
  },
  "/_content_live_live_goods": {
    "title": "商品管理",
    "topMenu": "应用端"
  },
  "/_content_live_add_live_goods": {
    "title": "添加直播商品",
    "topMenu": "应用端"
  },
  "/_content_live_anchor": {
    "title": "主播管理",
    "topMenu": "应用端"
  },
  "/live_anchor_add_<id>": {
    "title": "添加/修改主播表单",
    "topMenu": "应用端"
  },
  "/_app_pc": {
    "title": "PC 配置",
    "topMenu": "应用端"
  },
  "/_setting_pc_group_data": {
    "title": "PC商城",
    "topMenu": "应用端"
  },
  "/_app_app": {
    "title": "APP",
    "topMenu": "应用端"
  },
  "/_app_app_update": {
    "title": "版本管理",
    "topMenu": "应用端"
  },
  "/_work_config": {
    "title": "企微设置",
    "topMenu": "应用端"
  },
  "/_setting_base": {
    "title": "系统设置",
    "topMenu": "设置"
  },
  "/_setting_shop_base": {
    "title": "系统设置",
    "topMenu": "设置"
  },
  "/_setting_notification_index": {
    "title": "消息设置",
    "topMenu": "设置"
  },
  "/_setting_notification_notificationEdit": {
    "title": "消息设置",
    "topMenu": "设置"
  },
  "/_setting_service": {
    "title": "服务设置",
    "topMenu": "设置"
  },
  "/_setting_sms_sms_config_index": {
    "title": "一号通管理",
    "topMenu": "设置"
  },
  "/_setting_system_config_sms": {
    "title": "一号通配置",
    "topMenu": "设置"
  },
  "/_setting_third_party": {
    "title": "接口设置",
    "topMenu": "设置"
  },
  "/_setting_document": {
    "title": "小票打印",
    "topMenu": "设置"
  },
  "/_setting_shop_pay": {
    "title": "支付设置",
    "topMenu": "设置"
  },
  "/_setting_storage": {
    "title": "存储配置",
    "topMenu": "设置"
  },
  "/_setting_storage_index": {
    "title": "存储设置",
    "topMenu": "设置"
  },
  "/_setting_storage_thumbnail": {
    "title": "缩略图设置",
    "topMenu": "设置"
  },
  "/_setting_document_content": {
    "title": "小票打印",
    "topMenu": "设置"
  },
  "/_setting_auth_list": {
    "title": "权限设置",
    "topMenu": "设置"
  },
  "/_setting_system_role_index": {
    "title": "角色管理",
    "topMenu": "设置"
  },
  "/_setting_system_role_add": {
    "title": "添加身份",
    "topMenu": "设置"
  },
  "/_setting_system_admin_index": {
    "title": "管理员列表",
    "topMenu": "设置"
  },
  "/_setting_system_admin_add": {
    "title": "添加管理员",
    "topMenu": "设置"
  },
  "/_admin _setting_system_admin_edit": {
    "title": "编辑管理员",
    "topMenu": "设置"
  },
  "/_setting_system_menus_index": {
    "title": "权限规则",
    "topMenu": "设置"
  },
  "/_setting_system_menus_add": {
    "title": "添加规则",
    "topMenu": "设置"
  },
  "/_setting_system_menus_add_sub": {
    "title": "添加子菜单",
    "topMenu": "设置"
  },
  "/_setting_system_menus_edit": {
    "title": "修改权限",
    "topMenu": "设置"
  },
  "/_system_config": {
    "title": "开发配置",
    "topMenu": "设置"
  },
  "/_system_crontab": {
    "title": "定时任务",
    "topMenu": "设置"
  },
  "/_system_crontab_create": {
    "title": "添加定时任务",
    "topMenu": "设置"
  },
  "/_system_config_system_config_tab_index": {
    "title": "配置分类",
    "topMenu": "设置"
  },
  "/system_config_system_config_tab_edit": {
    "title": "编辑配置分类",
    "topMenu": "设置"
  },
  "/_system_config_system_group_index": {
    "title": "组合数据",
    "topMenu": "设置"
  },
  "/_system_config_system_config_tab_list": {
    "title": "配置列表",
    "topMenu": "设置"
  },
  "/_system_config_system_group_list": {
    "title": "组合数据列表",
    "topMenu": "设置"
  },
  "/_out": {
    "title": "对外接口",
    "topMenu": "设置"
  },
  "/_setting_other_out_config": {
    "title": "对外接口",
    "topMenu": "设置"
  },
  "/_out_interface": {
    "title": "接口文档",
    "topMenu": "设置"
  },
  "/_system_maintain": {
    "title": "安全维护",
    "topMenu": "设置"
  },
  "/_system_maintain_clear_index": {
    "title": "刷新缓存",
    "topMenu": "设置"
  },
  "/_system_maintain_system_log_index": {
    "title": "系统日志",
    "topMenu": "设置"
  },
  "/_system_maintain_system_file_index": {
    "title": "文件校验",
    "topMenu": "设置"
  },
  "/_system_maintain_system_cleardata_index": {
    "title": "清除数据",
    "topMenu": "设置"
  },
  "/_system_maintain_system_databackup_index": {
    "title": "数据备份",
    "topMenu": "设置"
  },
  "/_system_log": {
    "title": "系统日志",
    "topMenu": "设置"
  },
  "/_system_system_upgradeclient_index": {
    "title": "在线升级",
    "topMenu": "设置"
  },
  "/_setting_freight": {
    "title": "发货设置",
    "topMenu": "设置"
  },
  "/_system_user": {
    "title": "个人中心",
    "topMenu": "设置"
  },
  "/_system_maintain_auth": {
    "title": "商业授权",
    "topMenu": "设置"
  }
}

const visitedViews = ref([])
const activeTab = ref('')

watch(
  () => route.path,
  (newPath) => {
    if (newPath === '/' || newPath === '/login') return;
    
    // 1. Update Tags View
    const title = routeMetaMap[newPath]?.title || routeMetaMap[newPath.replace('/', '/_')]?.title || newPath.split('/').pop() || '首页'
    const existing = visitedViews.value.find(v => v.path === newPath)
    if (!existing) {
      visitedViews.value.push({ path: newPath, title })
    }
    activeTab.value = newPath

    // 2. Update Top Menu
    const topMenu = routeMetaMap[newPath]?.topMenu || routeMetaMap[newPath.replace('/', '/_')]?.topMenu
    if (topMenu && topMenu !== activeTopMenu.value) {
      activeTopMenu.value = topMenu
    }
  },
  { immediate: true }
)

const handleTabClick = (tab) => {
  router.push(tab.paneName)
}

const handleTabRemove = (targetName) => {
  const tabs = visitedViews.value
  let activeName = activeTab.value
  if (activeName === targetName) {
    tabs.forEach((tab, index) => {
      if (tab.path === targetName) {
        const nextTab = tabs[index + 1] || tabs[index - 1]
        if (nextTab) {
          activeName = nextTab.path
        }
      }
    })
  }
  activeTab.value = activeName
  visitedViews.value = tabs.filter((tab) => tab.path !== targetName)
  if (activeName !== targetName) {
    router.push(activeName)
  } else if (visitedViews.value.length === 0) {
    router.push('/')
  }
}

const handleTopMenuSelect = (index) => {
  activeTopMenu.value = index
}

const toggleTheme = () => {
  localStorage.setItem('ui_theme', 'v1')
  window.location.reload()
}

const logout = () => {
  localStorage.removeItem('admin_token')
  router.push('/login')
}

// Extract the menu HTML from the generated file to inject into sidebar
onMounted(async () => {
  try {
    // In a real scenario, this would be reactive based on top menu.
    // Here we fetch the generated_menu.html and apply slight CSS tweaks for light theme.
    const res = await fetch('/generated_menu.html')
    if(res.ok) {
      let html = await res.text()
      // Adjust standard element-plus dark menu to light menu classes or just rely on el-menu props
      sideMenuHtml.value = html
    }
  } catch(e) {
    console.error(e)
  }
})
</script>

<style scoped>
.layout-v2-container {
  height: 100vh;
  width: 100vw;
  display: flex;
  flex-direction: column;
}

.top-header {
  background-color: #3e75f5; /* Shows.mom blue header */
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px 0 0;
  color: white;
}

.header-logo {
  width: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #3567df;
  height: 100%;
}
.logo-img {
  height: 30px;
}


.top-nav {
  flex: 1;
  display: flex;
  align-items: center;
  min-width: 0; /* Important for flex child to shrink and overflow */
}

.top-nav-wrapper {
  display: flex;
  align-items: center;
  width: 100%;
  position: relative;
  overflow: hidden;
}

.nav-arrow {
  cursor: pointer;
  padding: 0 10px;
  color: #fff;
  display: flex;
  align-items: center;
  height: 60px;
  z-index: 2;
  transition: background 0.3s;
}
.nav-arrow:hover {
  background: rgba(255,255,255,0.1);
}

.top-nav-scroll {
  flex: 1;
  overflow-x: auto;
  overflow-y: hidden;
  scrollbar-width: none;
  -ms-overflow-style: none;
  scroll-behavior: smooth;
  white-space: nowrap;
}
.top-nav-scroll::-webkit-scrollbar {
  display: none;
}

.top-menu {
  border-bottom: none !important;
  height: 60px;
  display: inline-flex;
}

:deep(.el-menu--horizontal > .el-menu-item) {
  height: 60px;
  line-height: 60px;
  border-bottom: none !important;
  font-size: 15px;
  padding: 0 20px;
  color: rgba(255,255,255,0.7) !important;
  transition: all 0.3s;
}

:deep(.el-menu--horizontal > .el-menu-item:hover) {
  background-color: rgba(255, 255, 255, 0.1) !important;
  color: #fff !important;
}

:deep(.el-menu--horizontal > .el-menu-item.is-active) {
  color: #3e75f5 !important;
  background-color: #fff !important;
  font-weight: bold;
  border-radius: 8px 8px 0 0;
  height: 50px;
  line-height: 50px;
  margin-top: 10px;
}

:deep(.el-menu--horizontal > .el-menu-item:hover) {
  background-color: rgba(255,255,255,0.1) !important;
}

.header-actions {
  display: flex;
  align-items: center;
}

.action-icon {
  font-size: 18px;
  margin: 0 10px;
  cursor: pointer;
  color: #fff;
}
.action-icon:hover {
  opacity: 0.8;
}

.badge-icon {
  position: relative;
}
.badge-dot {
  position: absolute;
  top: -2px;
  right: -2px;
  width: 6px;
  height: 6px;
  background-color: #f56c6c;
  border-radius: 50%;
}

.platform-tag {
  margin: 0 15px;
  background-color: #fff;
  border: none;
}

.user-dropdown {
  display: flex;
  align-items: center;
  cursor: pointer;
  padding: 0 15px;
  color: white;
}
.user-avatar {
  margin-right: 8px;
}

.main-body {
  flex: 1;
  overflow: hidden;
  background-color: #f0f2f5;
}

.left-sidebar {
  background-color: #fff;
  border-right: 1px solid #e6e6e6;
  display: flex;
  flex-direction: column;
}

.sidebar-header {
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 15px;
  border-bottom: 1px solid #f0f0f0;
  font-weight: bold;
  color: #333;
}
.collapse-icon {
  cursor: pointer;
  color: #999;
}
.collapse-icon:hover {
  color: #3e75f5;
}


.side-menu {
  border-right: none;
  flex: 1;
  overflow-y: auto;
  background-color: #fff;
}




/* Fix root menu alignment */
:deep(.side-menu > .el-menu-item) {
  padding-left: 20px !important;
}
:deep(.side-menu > .el-sub-menu > .el-sub-menu__title) {
  padding-left: 20px !important;
}

/* Fix child menu alignment */
:deep(.el-menu--inline .el-menu-item) {
  padding-left: 50px !important;
  min-width: 0;
}
:deep(.el-menu--inline .el-sub-menu__title) {
  padding-left: 50px !important;
}
:deep(.el-menu--inline .el-menu--inline .el-menu-item) {
  padding-left: 65px !important;
}
:deep(.el-menu--inline .el-menu--inline .el-sub-menu__title) {
  padding-left: 65px !important;
}
:deep(.el-menu-item), :deep(.el-sub-menu__title) {
  margin: 4px 8px;
  border-radius: 4px;
  height: 40px;
  line-height: 40px;
  color: #606266;
}
:deep(.el-sub-menu__title) {
  padding-right: 30px; /* space for arrow */
}



:deep(.el-menu-item.is-active) {
  color: #3e75f5 !important;
  background-color: #eef2fe !important;
  font-weight: 500;
}

:deep(.el-sub-menu__title) {
  color: #303133 !important;
  font-weight: 500;
}

:deep(.el-sub-menu__title:hover),
:deep(.el-menu-item:hover) {
  background-color: #f5f7fa !important;
  color: #3e75f5 !important;
}

.sidebar-title {
  font-size: 16px;
  white-space: nowrap;
  overflow: hidden;
}


.content-area {
  padding: 15px;
  background-color: #f0f2f5;
  overflow-y: auto;
}


.tags-view-container {
  background: #fff;
  padding: 6px 15px 0;
  border-bottom: 1px solid #d8dce5;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.12), 0 0 3px 0 rgba(0, 0, 0, 0.04);
  margin-bottom: 15px;
}
:deep(.el-tabs__header) {
  margin: 0;
  border-bottom: none;
}
:deep(.el-tabs--card > .el-tabs__header .el-tabs__nav) {
  border: none;
}
:deep(.el-tabs--card > .el-tabs__header .el-tabs__item) {
  height: 30px;
  line-height: 30px;
  border: 1px solid #d8dce5;
  border-radius: 2px;
  margin-right: 5px;
  font-size: 12px;
  color: #495060;
  background: #fff;
  padding: 0 15px !important;
}
:deep(.el-tabs--card > .el-tabs__header .el-tabs__item.is-active) {
  color: #fff;
  background-color: #3e75f5;
  border-color: #3e75f5;
}

.page-container {
  min-height: 100%;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
