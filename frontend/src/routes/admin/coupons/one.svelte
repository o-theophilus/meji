<script>
	import { Tag } from '$lib/button';
	import { Datetime } from '$lib/macro';
	let { coupon } = $props();
</script>

<a href="/admin/coupons/{coupon.key}" class="one">
	<div class="row_1">
		<span>
			sn: {coupon.key.slice(-11, coupon.key.length)}
		</span>
		<span>
			<Datetime datetime={coupon.date_created} type="date_numeric" />
			<Datetime datetime={coupon.date_created} type="time_12h" />
		</span>
	</div>

	<div class="row_2">
		<div class="coupon_note">
			{@html coupon.note}
		</div>

		{#if coupon.status == 'used'}
			<Tag href="/orders/{coupon.order_key}" --tag-background-color="rgb(202, 202, 255)"
				>{coupon.status}</Tag
			>
		{:else}
			<Tag>{coupon.status}</Tag>
		{/if}
	</div>

	{#if coupon.valid_from}
		<div class="row_3">
			Validity:
			<Datetime datetime={coupon.valid_from} type="date_numeric" />
			<!-- <Datetime datetime={coupon.valid_from} type="time_12h" /> -->
			{#if coupon.valid_until}
				-
				<Datetime datetime={coupon.valid_until} type="date_numeric" />
				<!-- <Datetime datetime={coupon.valid_until} type="time_12h" /> -->
			{/if}
		</div>
	{/if}
</a>

<style>
	.one {
		display: block;

		margin-top: 8px;
		padding: 16px;
		background-color: var(--bg3);
		border-radius: 8px;

		text-decoration: none;
		color: var(--ft2);
		text-decoration: none;
		outline: 1px solid var(--ol);
		outline-offset: -1px;

		transition: background-color 0.2s ease-in-out;

		&:hover {
			background-color: var(--bg2);
		}

		& .row_1 {
			display: flex;
			justify-content: space-between;
			gap: 16px;

			font-size: 0.7em;
		}
		& .row_2 {
			margin-top: 8px;

			display: flex;
			justify-content: space-between;
			gap: 16px;

			--tag-font-size: 0.7rem;
		}
		& .row_3 {
			font-size: 0.7em;
		}
	}

	:global(.one .coupon_note .bold) {
		font-weight: 800;
		color: var(--ft1);
	}
</style>
