from django.shortcuts import render


def home(request):
    # plot = bokeh_test.get_coles_plot()
    # script, div = components(plot)
    # return render(request, 'home.html', {'script': script, 'div': div})
    return render(request, 'home.html', {})
