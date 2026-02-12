<script>
	import { BackButton, Button, RoundButton, Tag } from '$lib/button';
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
	<div class="block">
		<div class="row_1">
			<span>
				sn: {coupon.key.slice(-11, coupon.key.length)}
			</span>
			<span>
				<Datetime datetime={coupon.date_created} type="date_numeric" />
				<Datetime datetime={coupon.date_created} type="time_12h" />
			</span>
		</div>

		<div class="coupon_note">
			{@html coupon.note}
		</div>

		<div class="code">
			{#if show_code}
				{coupon.code.toUpperCase()}
			{:else}
				**********
			{/if}

			{#if app.user.access.includes('coupon:view_code')}
				<RoundButton icon={show_code ? 'eye' : 'eye-off'} onclick={() => (show_code = !show_code)}
				></RoundButton>
			{/if}
		</div>

		<div class="validity">
			Validity:
			{#if coupon.valid_from}
				<Datetime datetime={coupon.valid_from} type="date_numeric" />
				{#if coupon.valid_until}
					-
					<Datetime datetime={coupon.valid_until} type="date_numeric" />
				{/if}
			{:else}
				Unset
			{/if}
		</div>
	</div>

	{#if app.user.access.includes('coupon:edit_validity') || app.user.access.includes('coupon:delete')}
		<div class="line btns">
			{#if app.user.access.includes('coupon:edit_validity')}
				<Button onclick={() => module.open(Validity, { update, coupon })}>Validity</Button>
			{/if}
			{#if app.user.access.includes('coupon:delete')}
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
	.coupon_note {
		margin-top: 24px;
		text-align: center;
	}

	:global(.block .coupon_note .line_1) {
		line-height: 100%;
		font-weight: 800;
		color: var(--ft1);
		font-size: 2rem;

		& .bold {
			line-height: 100%;
		}
	}

	.line {
		--tag-font-size: 0.7rem;
	}

	.block {
		padding: 16px;
		background-color: var(--bg3);
		border-radius: 8px;

		outline: 1px solid var(--ol);
		outline-offset: -1px;

		& .row_1 {
			display: flex;
			justify-content: space-between;
			gap: 16px;

			font-size: 0.7em;
		}

		& .code {
			display: flex;
			gap: 8px;
			justify-content: center;
			align-items: center;

			margin-top: 24px;
			text-align: center;
			text-align: center;
			font-size: 1.2rem;
		}

		& .validity {
			text-align: center;
			margin-top: 12px;
			font-size: 0.7em;
		}
	}
	.btns {
		margin-top: 16px;
	}
</style>
