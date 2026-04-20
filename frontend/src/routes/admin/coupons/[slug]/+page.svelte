<script>
	import { Button, RoundButton } from '$lib/button';
	import { Content } from '$lib/layout';
	import { Datetime, Log, Meta } from '$lib/macro';
	import { app, module } from '$lib/store.svelte.js';
	import Delete from './_delete.svelte';
	import Validity from './_validity.svelte';
	let { data } = $props();
	let coupon = $derived(data.coupon);

	const update = (data) => {
		coupon = data;
	};

	let show_code = $state(false);
</script>

<Meta title="Coupon" />
<Log action={'viewed'} entity_key={coupon.key} entity_type={'user'} />

<Content --content-height="auto">
	<div class="line">
		<RoundButton icon="arrow-left" href="/admin/coupons"></RoundButton>
		<div class="page_title">Coupon</div>
	</div>
</Content>

<Content --content-padding-top="1px">
	<div class="coupon">
		<span class="id_date">
			id: {coupon.key.slice(-11, coupon.key.length)}
			<span>
				<Datetime datetime={coupon.date_created} type="date_numeric" />
				<Datetime datetime={coupon.date_created} type="time_12h" />
			</span>
		</span>

		<div class="coupon_page">
			{@html coupon.note}
		</div>

		<div class="code">
			{#if show_code}
				{coupon.code.toUpperCase()}
			{:else}
				**********
			{/if}

			{#if app.user.access.includes('coupon.view_code')}
				<RoundButton
					icon={show_code ? 'eye' : 'eye-off'}
					icon_size="12"
					--button-width_="24px"
					--button-height_="24px"
					onclick={() => (show_code = !show_code)}
				></RoundButton>
			{/if}
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
	</div>

	{#if (app.user.access.includes('coupon.edit_validity') || app.user.access.includes('coupon.delete')) && coupon.status != 'used'}
		<div class="line btns">
			{#if app.user.access.includes('coupon.edit_validity')}
				<Button onclick={() => module.open(Validity, { update, coupon })}>Validity</Button>
			{/if}
			{#if app.user.access.includes('coupon.delete')}
				<Button
					icon="trash-2"
					--button-background-color="darkred"
					--button-background-color-hover="red"
					--button-color-hover="hsl(0, 0%, 95%)"
					onclick={() => module.open(Delete, { coupon })}>Delete</Button
				>
			{/if}
		</div>
	{/if}
</Content>

<style>
	.coupon {
		padding: 24px;
		background-color: var(--bg3);
		border-radius: 8px;

		outline: 1px solid var(--ol);
		align-items: center;
		outline-offset: -1px;
		text-align: center;

		& .id_date {
			display: flex;
			justify-content: space-between;
			flex-wrap: wrap;
			gap: 0 16px;

			font-size: 0.7em;
		}

		& .coupon_page {
			margin: 12px 0;
		}

		& .code {
			display: flex;
			gap: 8px;
			justify-content: center;
			align-items: center;

			font-size: 1.2rem;
			margin: 12px 0;
			padding: 8px 8px 8px 16px;
			outline: 1px solid var(--ol);
			border-radius: 8px;
			background-color: var(--bg2);
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

	:global(.coupon_page) {
		& .line_1 {
			font-weight: 800;
			color: var(--ft1);
			font-size: 1.2rem;
		}
	}

	.btns {
		margin-top: 16px;
	}
</style>
