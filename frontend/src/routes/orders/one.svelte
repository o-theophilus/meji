<script>
	import { Datetime } from '$lib/macro';

	let { order } = $props();
</script>

<a href="/orders/{order.key}">
	<div class="line space">
		<div class="order_id">
			ID: {order.key.substring(0, 8)}
		</div>
		<div class="items">
			{order.item_count} item{order.item_count > 1 ? 's' : ''}
		</div>
		<div class="date">
			<Datetime datetime={order.date_created} type="date_numeric" />
			<Datetime datetime={order.date_created} type="time_12h" />
		</div>
	</div>

	<div class="line space">
		<div class="left">
			<div class="name">
				{order.name}
			</div>
			<div class="username">
				@{order.username}
			</div>
		</div>
		<div class="total">
			₦{Number(order.pay_user).toLocaleString()}
		</div>
	</div>
</a>

<style>
	a {
		display: block;

		margin: 8px 0;
		padding: 16px;
		border-radius: 8px;

		background-color: var(--bg3);
		text-decoration: none;
		color: var(--ft2);
		outline: 1px solid var(--ol);
		outline-offset: -1px;

		transition: background-color 0.2s ease-in-out;

		&:hover {
			background-color: var(--bg2);
		}
	}
	.order_id {
		font-weight: 800;
	}
	.items,
	.date {
		font-size: 0.7rem;
	}

	.name {
		font-size: 0.8rem;
		font-weight: 800;
		color: var(--ft1);
	}
	.username {
		font-size: 0.7rem;
	}
	.total {
		font-weight: 800;
		color: var(--ft1);
	}
</style>
