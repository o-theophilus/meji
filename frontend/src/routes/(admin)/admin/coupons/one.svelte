<script>
	import { Datetime } from '$lib/macro';
	let { coupon } = $props();
</script>

<a href="/admin/coupons/{coupon.key}" class="coupon">
	<span class="id_date">
		id: {coupon.key.slice(-11, coupon.key.length)}

		<span>
			<Datetime datetime={coupon.date_created} type="date_numeric" />
			<Datetime datetime={coupon.date_created} type="time_12h" />
		</span>
	</span>

	<div class="coupon_one">
		{@html coupon.note}
	</div>

	<span class="validity">
		Validity:
		{#if coupon.valid_from && coupon.valid_until}
			<Datetime datetime={coupon.valid_from} type="date_numeric" />
			-
			<Datetime datetime={coupon.valid_until} type="date_numeric" />
		{/if}

		&nbsp;
		<span class="status" class:active={coupon.status == 'active'}>
			{coupon.status}
		</span>
	</span>
</a>

<style>
	.coupon {
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

		& .id_date {
			display: flex;
			justify-content: space-between;
			flex-wrap: wrap;
			gap: 0 16px;

			font-size: 0.7em;
		}

		& .coupon_one {
			margin: 12px 0;
		}

		& .validity {
			font-size: 0.7em;

			& .status {
				outline: 1px solid color-mix(in srgb, red, transparent 70%);
				background-color: color-mix(in srgb, red, transparent 90%);
				color: red;
				padding: 2px 4px;
				border-radius: 10px;

				&.active {
					outline: 1px solid color-mix(in srgb, green, transparent 70%);
					background-color: color-mix(in srgb, green, transparent 90%);
					color: green;
				}
			}
		}
	}

	:global(.coupon_one) {
		& .line_1 {
			font-weight: 800;
			color: var(--ft1);
		}
	}
</style>
