<script>
	import { goto } from '$app/navigation';
	import { Login } from '$lib/auth';
	import { Button } from '$lib/button';
	import { Dialogue, Note } from '$lib/info';
	import { app, loading, module, scroll } from '$lib/store.svelte.js';
	import { onMount } from 'svelte';
	import Email_Admin from '../orders/[slug]/status.create.email.admin.svelte';
	import Email_User from '../orders/[slug]/status.create.email.user.svelte';
	let email_template_admin;
	let email_template_user;

	let paystack;
	onMount(async () => {
		const module = await import('@paystack/inline-js');
		let Paystack = module.default;
		paystack = new Paystack();
	});

	let { ops = $bindable() } = $props();

	const make_payment = async () => {
		ops.error = {};
		loading.open('Loading . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/order/check`, {
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			}
		});
		resp = await resp.json();
		loading.close();

		if (resp.status == 200) {
			paystack.checkout({
				key: import.meta.env.VITE_PAYSTACK_KEY,
				email: app.user.email,
				amount: resp.pay * 100,

				onLoad: (response) => {
					console.log('onLoad: ', response);
				},
				onCancel: () => {
					module.open(Dialogue, {
						status: 400,
						title: 'Payment Canceled',
						message: `The payment process was canceled`,
						buttons: [
							{
								name: 'Ok',
								icon: 'ok',
								fn: () => {
									module.close();
								}
							}
						]
					});
				},
				onError: (error) => {
					module.open(Dialogue, {
						status: 400,
						title: 'Payment Error',
						message: error.message,
						buttons: [
							{
								name: 'Ok',
								icon: 'ok',
								fn: () => {
									module.close();
								}
							}
						]
					});
				},
				onSuccess: (transaction) => {
					console.log(transaction);
					submit(transaction.reference);
				}
			});
		} else {
			ops.error = resp;
		}
	};

	const submit = async (reference) => {
		ops.error = {};

		loading.open('Loading . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/order`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			},
			body: JSON.stringify({
				reference,
				email_template_admin: email_template_admin.innerHTML.replace(/&amp;/g, '&'),
				email_template_user: email_template_user.innerHTML.replace(/&amp;/g, '&')
			})
		});
		resp = await resp.json();
		loading.close();

		if (resp.status == 200) {
			app.cart_items = [];
			page_state.clear('cart');
			goto(`/orders/${resp.order.key}`);

			module.open(Dialogue, {
				status: 200,
				title: 'Successful',
				message: `Your order was placed successfully`,
				buttons: [
					{
						name: 'Ok',
						icon: 'ok',
						fn: () => {
							module.close();
						}
					}
				]
			});
		} else {
			ops.error = resp;
		}
	};

	let pay = $derived.by(() => {
		let sum = ops.total_order;
		if (ops.has_receiver) {
			sum += Number(ops.cart.delivery_cost);
		}
		if (ops.coupon && ops.discount_condition_met) {
			sum -= ops.discount;
		}

		return Math.max(sum, 0);
	});
</script>

<div class="floater">
	<div class="floater_block">
		<div class="line space">
			<div class="total">Total Amount</div>
			<div class="cost">
				₦{pay.toLocaleString()}
			</div>
		</div>

		<div class="checkout">
			<Button
				icon="cart"
				--button-background-color="var(--cl1)"
				--button-background-color-hover="color-mix(in srgb, var(--cl1), black 50%)"
				--button-color="hsl(0, 0%, 95%)"
				--button-color-hover="hsl(0, 0%, 95%)"
				onclick={() => {
					if (!app.login) {
						module.open(Login);
					} else if (!ops.item_ckeck) {
						ops.status = 'Items';
						ops.error.error = 'Kindly check the items for error';
						scroll('#Items');
					} else if (!ops.has_receiver) {
						ops.status = 'Receiver';
						ops.error.error = 'Please provide receiver information before checkout';
						scroll('#Receiver');
					} else if (!ops.agree) {
						ops.error.error = 'Please agree to the terms and conditions to proceed';
						scroll('#terms');
					} else {
						make_payment();
					}
				}}
			>
				{#if !app.login}
					Login to
				{/if}
				Checkout
			</Button>
		</div>

		<Note note={ops.error.error} status="400" --note-margin-top="16px"></Note>
	</div>
</div>

<div bind:this={email_template_admin} style="display: none;">
	<Email_Admin order={ops.cart} items={app.cart_items} />
</div>
<div bind:this={email_template_user} style="display: none;">
	<Email_User order={ops.cart} items={app.cart_items} />
</div>

<style>
	.floater {
		position: sticky;
		bottom: var(--headerHeight);

		background-color: var(--bg);
		border-top: 1px solid var(--ol);

		@media screen and (min-width: 800px) {
			bottom: 0;
		}
	}

	.floater_block {
		padding: 16px 24px;
		max-width: var(--pageWidth);
		margin: auto;
	}

	.total {
		font-size: 0.8rem;
	}
	.cost {
		font-weight: 700;
		font-size: 1.2rem;
		color: var(--ft1);
	}

	.checkout {
		display: flex;
		justify-content: flex-end;
		margin-top: 16px;
	}
</style>
