<script>
	import { BackButton, Button, Tag } from '$lib/button';
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
</script>

<Meta title="Coupon" />
<Log action={'viewed'} entity_key={coupon.key} entity_type={'user'} />

<Content --content-height="auto">
	<div class="line space">
		<div class="line">
			<BackButton />
			<div class="page_title">Coupon</div>
		</div>
		{#if coupon.status == 'used'}
			<Tag --tag-background-color="rgb(202, 202, 255)">{coupon.status}</Tag>
		{:else}
			<Tag>{coupon.status}</Tag>
		{/if}
	</div>
</Content>

<Content --content-padding-top="1px">
	<div class="one">
		<div class="row_1">
			<span>
				sn: {coupon.key.slice(-11, coupon.key.length)}
			</span>
			<span>
				<Datetime datetime={coupon.date_created} type="date_numeric" />
				<Datetime datetime={coupon.date_created} type="time_12h" />
			</span>
		</div>

		<div class="benefit">
			<span class="offer">
				{#if coupon.benefit.value_unit == 'percent'}
					{coupon.benefit.value}% discount
				{:else if coupon.benefit.value_unit == 'flat'}
					₦{Number(coupon.benefit.value).toLocaleString()}
					off
				{/if}
				on
				{#if coupon.benefit.for == 'delivery'}
					{coupon.benefit.for} fee
				{:else if coupon.benefit.for == 'order'}
					{coupon.benefit.for}
				{/if}
			</span>

			{#if coupon.benefit.threshold_unit && coupon.benefit.threshold}
				<br />
				for {coupon.benefit.threshold_unit}s above ₦{Number(
					coupon.benefit.threshold
				).toLocaleString()}
			{/if}

			<br />

			<div class="code">
				{coupon.code.toUpperCase()}
			</div>

			<div class="validity">
				Validity:
				{#if coupon.valid_from}
					<Datetime datetime={coupon.valid_from} type="date_numeric" />
					<!-- <Datetime datetime={coupon.valid_from} type="time_12h" /> -->
					{#if coupon.valid_until}
						-
						<Datetime datetime={coupon.valid_until} type="date_numeric" />
						<!-- <Datetime datetime={coupon.valid_until} type="time_12h" /> -->
					{/if}
				{:else}
					Unset
				{/if}
			</div>
		</div>
	</div>

	{#if app.user.access.includes('coupon:edit_validity') || app.user.access.includes('coupon:delete')}
		<div class="line btns">
			{#if app.user.access.includes('coupon:edit_validity')}
				<Button onclick={() => module.open(Validity, { update, coupon })}>Validity</Button>
			{/if}
			{#if app.user.access.includes('coupon:delete')}
				<Button icon="trash-2" onclick={() => module.open(Delete, { coupon })}>Delete</Button>
			{/if}
		</div>
	{/if}
</Content>

<style>
	.line {
		--tag-font-size: 0.7rem;
	}

	.one {
		padding: 16px;
		background-color: var(--bg3);
		border-radius: 8px;

		text-decoration: none;
		color: var(--ft2);
		text-decoration: none;
		outline: 1px solid var(--ol);
		outline-offset: -1px;

		& .row_1 {
			display: flex;
			justify-content: space-between;
			gap: 16px;

			font-size: 0.7em;
		}

		.benefit {
			margin-top: 24px;
			text-align: center;

			& .offer {
				line-height: 100%;
				font-weight: 800;
				color: var(--ft1);
				font-size: 2rem;
			}

			& .code {
				margin-top: 24px;
				text-align: center;
				font-size: 1.2rem;
			}

			& .validity {
				margin-top: 12px;
				font-size: 0.7em;
			}
		}
	}
	.btns {
		margin-top: 16px;
	}
</style>
