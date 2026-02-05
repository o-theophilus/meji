<script>
	import { Icon } from '$lib/macro';

	let { list, size } = $props();
	let time = $state('0.2s');
	let n = $state(0);

	const scroll = (dir) => {
		if (dir == 'left') n -= 1;
		if (dir == 'right') n += 1;
		else if (typeof dir === 'number') n = dir;

		if (n > list.length) {
			n = 0;
			time = '0';
			setTimeout(() => {
				n = 1;
				time = '0.2s';
			}, 0);
		} else if (n < 0) {
			n = list.length;
			time = '0';
			setTimeout(() => {
				n = list.length - 1;
				time = '0.2s';
			}, 0);
		}
		resetAutoScroll();
	};

	let autoScroll;
	const resetAutoScroll = () => {
		clearTimeout(autoScroll);
		autoScroll = setTimeout(() => {
			scroll('right');
			resetAutoScroll();
		}, 6000);
	};

	resetAutoScroll();
</script>

{#if list.length}
	<section id="advert">
		<div class="scroller" style:--pos={n} style:--time={time}>
			{#each list as ads, i}
				<a href="/{ads.slug}">
					<img
						src={ads.photo[size] || '/no_photo.png'}
						alt={ads.name}
						onerror={(e) => (e.target.src = '/no_photo.png')}
					/>
				</a>
			{/each}
			{#if list[0].photo[size]}
				<a href="/{list[0].slug}">
					<img
						src={list[0].photo[size] || '/no_photo.png'}
						alt={list[0].name}
						onerror={(e) => (e.target.src = '/no_photo.png')}
					/>
				</a>
			{/if}
		</div>

		<div class="left">
			<button onclick={() => scroll('left')}>
				<Icon icon="arrow-left"></Icon>
			</button>
		</div>
		<div class="right">
			<button onclick={() => scroll('right')}>
				<Icon icon="arrow-right"></Icon>
			</button>
		</div>

		<div class="bottom">
			<div class="points">
				{#each Array(list.length) as _, i}
					<button class:active={n == i || (i == 0 && n == list.length)} onclick={() => scroll(i)}>
						<div>.</div>
					</button>
				{/each}
			</div>
		</div>
	</section>
{/if}

<style>
	section {
		position: relative;
		border-radius: 8px;
		overflow: hidden;

		margin-top: var(--advert-margin-top, 0);
		margin-bottom: var(--advert-margin-bottom, 0);

		& .scroller {
			display: flex;
			transform: translate(calc(var(--pos) * -100%));
			transition: transform var(--time) ease-in-out;

			& a {
				flex: 0 0 100%;

				& img {
					display: block;
					width: 100%;
				}
			}
		}
	}

	.left,
	.right {
		position: absolute;
		top: 0;
		bottom: 0;
		left: 4px;

		display: flex;
		align-items: center;
		pointer-events: none;

		& button {
			all: unset;
			cursor: pointer;
			pointer-events: all;

			display: flex;
			align-items: center;
			justify-content: center;
			background-color: hsla(0, 0%, 0%, 0.1);
			color: hsla(0, 0%, 100%, 0.3);

			width: 32px;
			height: 56px;
			border-radius: 4px;

			transition:
				background-color 0.2s ease-in-out,
				color 0.2s ease-in-out;

			&:hover {
				background-color: hsla(0, 0%, 0%, 0.3);
				color: hsla(0, 0%, 95%);
			}
		}
	}
	.right {
		left: unset;
		right: 4px;
	}

	.bottom {
		position: absolute;
		right: 0;
		left: 0;
		bottom: 4px;
		pointer-events: none;

		display: flex;
		justify-content: center;

		& .points {
			display: flex;
			gap: 8px;
			border-radius: 50px;

			padding: 8px;
			background-color: hsla(0, 0%, 0%, 0.1);
			pointer-events: all;

			& button {
				all: unset;
				cursor: pointer;

				--size: 8px;
				width: var(--size);
				height: var(--size);
				border-radius: 50px;

				background-color: hsla(0, 0%, 100%, 0.2);

				line-height: 0;
				color: transparent;

				transition:
					background-color 0.2s ease-in-out,
					width 0.2s ease-in-out;

				& div {
					height: 100%;

					width: 0%;
					background-color: hsla(0, 0%, 95%, 0.5);
				}

				&.active {
					width: calc(var(--size) * 3);
					overflow: hidden;

					& div {
						transition: width 6s linear;
						width: 100%;
					}
				}
				&:not(.active):hover {
					background-color: hsla(0, 0%, 95%, 0.6);
				}
			}
		}
	}
</style>
