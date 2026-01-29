<script>
	import { Datetime } from '$lib/macro';

	let { order } = $props();
</script>

<a href="/orders/{order.key}">
	<div class="date">
		<Datetime datetime={order.date_created} type="date_numeric" />
		<Datetime datetime={order.date_created} type="time_12h" />
	</div>
	<div>
		{order.key.substring(0, 8)}
	</div>
	<div>
		₦{Number(order.pay_user).toLocaleString()}
	</div>
</a>

<style>
	a {
		display: block;

		margin: var(--sp1) 0;
		padding: var(--sp2);
		border-radius: 8px;

		background-color: var(--bg);
		text-decoration: none;
		color: var(--ft2);
		outline: 2px solid transparent;
		outline-offset: -2px;

		transition: outline-color var(--trans);
	}
	a:hover {
		outline-color: var(--ft2);
	}

	.date {
		font-size: 0.7rem;
		color: var(--ft2);
	}
</style>
