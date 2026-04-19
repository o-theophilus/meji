<script>
	import { Button } from '$lib/button';
	import { Note } from '$lib/info';
	import { Card } from '$lib/layout';
	import { Datetime } from '$lib/macro';
	import { module } from '$lib/store.svelte.js';
	import { slide } from 'svelte/transition';
	import Add from './_add.svelte';
	import Remove from './_remove.svelte';

	let { ops = $bindable() } = $props();
	let name = 'Coupon';

	let error = $derived.by(() => {
		let temp = {};
		if (!ops.coupon) return temp;

		if (ops.coupon.status == 'inactive') {
			temp.status = 400;
			temp.note = 'This coupon will not apply as it is no longer active';
		} else if (ops.coupon.status == 'expired') {
			temp.status = 400;
			temp.note = 'This coupon will not apply as it has expired';
		} else if (!ops.discount_condition_met) {
			temp.status = 201;
			temp.note = `This coupon will not apply as <b>${ops.coupon.benefit.condition_unit}</b> is not up to
				<b>₦${Number(ops.coupon.benefit.condition).toLocaleString()}</b>`;
		}
		return temp;
	});
</script>

<Card
	--card-background-color="var(--bg3_)"
	open={ops.status == name}
	onclick={() => {
		ops.status = ops.status != name ? name : null;
	}}
>
	{#snippet title()}
		<div class="line space">
			<div class="title">{name}</div>

			<div class="line">
				{#if !ops.coupon}
					<Button
						--button-height="42px"
						--button-font-size="0.8rem"
						icon="plus"
						onclick={() => module.open(Add, { ops })}>Add</Button
					>
				{:else if ops.status != name}
					<div class="c">
						<div class="a">Discount</div>
						<div class="b" transition:slide>
							{#if ops.discount_condition_met}
								{#if ops.discount}
									-
								{/if}

								₦{Number(ops.discount).toLocaleString()}
							{:else}
								0
							{/if}
						</div>
					</div>
				{/if}
			</div>
		</div>
	{/snippet}

	{#if ops.coupon}
		<div class="coupon">
			<div class="frame top right"></div>
			<div class="frame top left"></div>
			<div class="frame bottom right"></div>
			<div class="frame bottom left"></div>
			<div class="frame bg"></div>

			<span class="id">
				id: {ops.coupon.key.slice(-11, ops.coupon.key.length)}
			</span>

			<div class="coupon_cart">
				{@html ops.coupon.note}
			</div>

			<span class="validity">
				Validity:
				{#if ops.coupon.valid_from && ops.coupon.valid_until}
					<Datetime datetime={ops.coupon.valid_from} type="date_numeric" />
					-
					<Datetime datetime={ops.coupon.valid_until} type="date_numeric" />
				{/if}

				&nbsp;
				<span class="status" class:active={ops.coupon.status == 'active'}>
					{ops.coupon.status}
				</span>
			</span>
		</div>

		{#if Object.keys(error).length}
			<Note note={error.title} status={error.status} --note-margin-top="16px">
				{@html error.note}
			</Note>
		{/if}

		<Button icon="trash-2" onclick={() => module.open(Remove, { ops })}>Remove Coupon</Button>
		<!-- {:else} -->
		<!-- <Button icon="square-pen" onclick={() => module.open(Add, { ops })}>Add Coupon</Button> -->
	{/if}

	<div class="line space total">
		<span class="a"> Discount</span>
		<div class="b">
			{#if ops.discount_condition_met}
				{#if ops.discount}
					-
				{/if}
				₦{Number(ops.discount).toLocaleString()}
			{:else}
				0
			{/if}
		</div>
	</div>
</Card>

<style>
	.title {
		font-size: 1.2rem;
	}

	.c {
		display: flex;
		flex-direction: column;
		align-items: flex-end;
	}
	.a {
		font-size: 0.8rem;
	}
	.b {
		font-weight: bold;
		font-size: 1.2rem;
		color: var(--ft1);
	}
	.total {
		/* margin-top: 16px; */
		padding-top: 16px;
		border-top: 1px solid var(--bg1);
	}

	.coupon {
		margin-bottom: 16px;
		border-radius: 8px;
		width: fit-content;
		padding: 24px;
		text-align: center;

		& .id {
			display: flex;
			justify-content: center;
			gap: 16px;
			font-size: 0.7rem;

			--tag-background-color: rgb(202, 202, 255);
		}

		& .coupon_cart {
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

		position: relative;
		overflow: hidden;
		--size: 52px;
		z-index: 0;

		& .frame {
			position: absolute;

			outline: 1px solid var(--ol);
			outline-offset: -1px;
		}

		& .bg {
			inset: 0;
			z-index: -1;
			background-color: var(--bg3);
		}

		& .top {
			top: calc(var(--size) / -2);
			border-radius: 50%;
			width: var(--size);
			height: var(--size);
			background-color: var(--bg2);
		}
		& .right {
			right: calc(var(--size) / -2);
		}
		& .bottom {
			bottom: calc(var(--size) / -2);
			border-radius: 50%;
			width: var(--size);
			height: var(--size);
			background-color: var(--bg2);
		}
		& .left {
			left: calc(var(--size) / -2);
		}
	}

	:global(.coupon_cart) {
		& .line_1 {
			font-weight: 800;
			color: var(--ft1);
			font-size: 1.2rem;
		}
	}
</style>
