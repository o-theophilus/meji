<script>
	import Button from '$lib/button.svelte';
	import SVG from '$lib/svg.svelte';
</script>

<div class="block">
	<a href="tel:+2348067397793">
		<SVG type="phone" />
		+234 806 739 7793</a
	>
	<a href="mailto:theophilus.ogbolu@gmail.com">
		<SVG type="email" />
		theophilus.ogbolu@gmail.com
	</a>
	<a
		href="https://www.google.com/maps/place/Igando+Bus+Stop/@6.5513295,3.2380606,17z/data=!3m1!4b1!4m5!3m4!1s0x103b8540d0692809:0x4a45a882b29213a8!8m2!3d6.5513242!4d3.2402439"
		target="blank"
	>
		<SVG type="location" />
		Lagos, Nigeria.
	</a>
</div>

<style>
	a {
		display: flex;
		align-items: center;
		gap: var(--sp1);

		width: fit-content;

		color: var(--ac2);
		fill: currentColor;
		text-decoration: none;
		font-weight: 500;
	}

	:hover {
		color: var(--cl1);
	}
</style>
